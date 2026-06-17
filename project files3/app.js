/**
 * VoteChain — Decentralized Voting DApp
 * Connects to MetaMask, interacts with Voting.sol via ethers.js
 */

// ─── CONTRACT CONFIG ─────────────────────────────────────────────────────────
// Replace CONTRACT_ADDRESS after deploying Voting.sol to your network
const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // ← paste deployed address

const CONTRACT_ABI = [
  // View functions
  "function electionTitle() view returns (string)",
  "function votingOpen() view returns (bool)",
  "function votingStart() view returns (uint256)",
  "function votingEnd() view returns (uint256)",
  "function totalVotes() view returns (uint256)",
  "function candidateCount() view returns (uint256)",
  "function admin() view returns (address)",
  "function hasVoted(address) view returns (bool)",
  "function voterChoice(address) view returns (uint256)",
  "function getAllCandidates() view returns (tuple(uint256 id, string name, string party, string manifesto, uint256 voteCount, bool exists)[])",
  "function getWinner() view returns (tuple(uint256 id, string name, string party, string manifesto, uint256 voteCount, bool exists))",
  "function getRemainingTime() view returns (uint256)",
  "function getElectionInfo() view returns (string title, bool isOpen, uint256 start, uint256 end, uint256 votes, uint256 numCandidates, address adminAddr)",
  // State-changing functions
  "function vote(uint256 _candidateId)",
  "function addCandidate(string _name, string _party, string _manifesto)",
  "function startVoting(uint256 _durationMinutes)",
  "function endVoting()",
  // Events
  "event VoteCast(address indexed voter, uint256 indexed candidateId, uint256 timestamp)",
  "event CandidateAdded(uint256 indexed candidateId, string name, string party)",
  "event VotingStarted(uint256 startTime, uint256 endTime)",
  "event VotingEnded(uint256 endTime, uint256 totalVotes)",
];

// ─── DEMO DATA (used when CONTRACT_ADDRESS is not set) ───────────────────────
const DEMO_CANDIDATES = [
  { id: 1n, name: "Alexandra Reyes", party: "Progressive Alliance",  manifesto: "Championing renewable energy, universal healthcare, and a living wage for all citizens.",           voteCount: 142n, exists: true },
  { id: 2n, name: "Marcus Bennett",  party: "Liberty First",         manifesto: "Lower taxes, deregulation, and strong border security to restore economic freedom.",                  voteCount:  89n, exists: true },
  { id: 3n, name: "Priya Sharma",    party: "Future Forward",        manifesto: "Technology-driven governance, open innovation, and evidence-based policy for the digital age.",      voteCount: 213n, exists: true },
  { id: 4n, name: "Daniel Okafor",   party: "Community Coalition",   manifesto: "Grassroots democracy, community ownership, and rebuilding trust between citizens and institutions.", voteCount:  67n, exists: true },
];

// ─── APP STATE ───────────────────────────────────────────────────────────────
const state = {
  provider:     null,
  signer:       null,
  contract:     null,
  address:      null,
  network:      null,
  isDemo:       true,
  hasVoted:     false,
  votedFor:     null,
  candidates:   [],
  electionInfo: {},
  txLog:        [],
  countdownId:  null,
  pollId:       null,
};

// ─── ELEMENTS ────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);

const els = {
  connectBtn:       $("connectBtn"),
  connectBtnLarge:  $("connectBtnLarge"),
  networkBadge:     $("networkBadge"),
  networkName:      $("networkName"),
  netDot:           document.querySelector(".net-dot"),
  walletBar:        $("walletBar"),
  walletAddress:    $("walletAddress"),
  voteStatusBadge:  $("voteStatusBadge"),
  voteStatusText:   $("voteStatusText"),
  connectPrompt:    $("connectPrompt"),
  electionTitle:    $("electionTitle"),
  electionStatus:   $("electionStatus"),
  totalVotes:       $("totalVotes"),
  timeRemaining:    $("timeRemaining"),
  candidatesSection:$("candidatesSection"),
  candidatesGrid:   $("candidatesGrid"),
  resultsSection:   $("resultsSection"),
  resultsContainer: $("resultsContainer"),
  txSection:        $("txSection"),
  txLog:            $("txLog"),
  voteModal:        $("voteModal"),
  modalClose:       $("modalClose"),
  modalCancel:      $("modalCancel"),
  modalConfirm:     $("modalConfirm"),
  modalCandidateName: $("modalCandidateName"),
  modalCandidateParty:$("modalCandidateParty"),
  modalCandidateId:   $("modalCandidateId"),
  modalNetwork:       $("modalNetwork"),
  confirmBtnText:     $("confirmBtnText"),
  confirmSpinner:     $("confirmSpinner"),
  toastContainer:     $("toastContainer"),
};

// ─── INIT ─────────────────────────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  setupListeners();
  loadDemoMode();
});

function setupListeners() {
  els.connectBtn.addEventListener("click", connectWallet);
  els.connectBtnLarge.addEventListener("click", connectWallet);
  els.modalClose.addEventListener("click", closeModal);
  els.modalCancel.addEventListener("click", closeModal);
  els.modalConfirm.addEventListener("click", submitVote);

  // Close modal on overlay click
  els.voteModal.addEventListener("click", e => {
    if (e.target === els.voteModal) closeModal();
  });
}

// ─── DEMO MODE ───────────────────────────────────────────────────────────────
function loadDemoMode() {
  state.isDemo    = true;
  state.candidates = DEMO_CANDIDATES;

  state.electionInfo = {
    title:         "2024 Community Leadership Election",
    isOpen:        true,
    totalVotes:    511n,
    numCandidates: 4n,
  };

  updateElectionHero();
  renderCandidates();
  renderResults();
  startDemoCountdown();
}

// ─── WALLET CONNECTION ────────────────────────────────────────────────────────
async function connectWallet() {
  if (!window.ethereum) {
    toast("MetaMask not detected. Please install the MetaMask extension.", "error");
    return;
  }

  try {
    toast("Requesting wallet access…", "info");
    state.provider = new ethers.BrowserProvider(window.ethereum);
    const accounts = await state.provider.send("eth_requestAccounts", []);

    if (!accounts.length) {
      toast("No accounts found. Unlock MetaMask.", "error");
      return;
    }

    state.signer  = await state.provider.getSigner();
    state.address = await state.signer.getAddress();
    state.network = await state.provider.getNetwork();

    updateWalletUI();

    // Try connecting to actual contract
    const isRealContract = CONTRACT_ADDRESS !== "0x0000000000000000000000000000000000000000";

    if (isRealContract) {
      await initContract();
    } else {
      state.isDemo = false; // Connected but no contract — stay on demo data
      toast("Wallet connected! Running with demo data (no contract deployed).", "info");
      checkDemoVoteStatus();
    }

    // Listen for account/network changes
    window.ethereum.on("accountsChanged", handleAccountsChanged);
    window.ethereum.on("chainChanged",    () => window.location.reload());

  } catch (err) {
    console.error(err);
    if (err.code === 4001) {
      toast("Connection rejected by user.", "error");
    } else {
      toast("Failed to connect: " + (err.message || err), "error");
    }
  }
}

async function initContract() {
  try {
    state.contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, state.signer);

    // Quick test call
    await state.contract.electionTitle();
    state.isDemo = false;

    toast("Connected to VoteChain contract ✓", "success");
    await refreshContractData();
    startPolling();
    subscribeToEvents();

  } catch (err) {
    console.error("Contract init failed:", err);
    toast("Contract not found on this network. Showing demo data.", "info");
    state.isDemo = true;
    state.contract = null;
    checkDemoVoteStatus();
  }
}

function handleAccountsChanged(accounts) {
  if (!accounts.length) {
    toast("Wallet disconnected.", "info");
    window.location.reload();
  } else {
    state.address = accounts[0];
    updateWalletUI();
    if (state.contract) refreshContractData();
  }
}

// ─── CONTRACT DATA ────────────────────────────────────────────────────────────
async function refreshContractData() {
  if (!state.contract) return;

  try {
    const [info, candidates, voted] = await Promise.all([
      state.contract.getElectionInfo(),
      state.contract.getAllCandidates(),
      state.contract.hasVoted(state.address),
    ]);

    state.electionInfo = {
      title:         info.title,
      isOpen:        info.isOpen,
      votingEnd:     Number(info.end),
      totalVotes:    info.votes,
      numCandidates: info.numCandidates,
    };

    state.candidates = candidates;
    state.hasVoted   = voted;

    if (voted) {
      state.votedFor = Number(await state.contract.voterChoice(state.address));
    }

    updateElectionHero();
    renderCandidates();
    renderResults();
    updateVoteStatusUI();

    if (state.electionInfo.isOpen && state.electionInfo.votingEnd) {
      startContractCountdown(state.electionInfo.votingEnd);
    }

  } catch (err) {
    console.error("Failed to fetch contract data:", err);
    toast("Error reading from blockchain.", "error");
  }
}

// ─── EVENTS ──────────────────────────────────────────────────────────────────
function subscribeToEvents() {
  if (!state.contract) return;

  state.contract.on("VoteCast", (voter, candidateId, timestamp) => {
    console.log("VoteCast event:", voter, candidateId);
    refreshContractData();
    if (voter.toLowerCase() === state.address.toLowerCase()) {
      toast("Your vote has been confirmed on-chain! 🎉", "success");
    }
  });
}

function startPolling() {
  if (state.pollId) clearInterval(state.pollId);
  state.pollId = setInterval(refreshContractData, 15000); // every 15s
}

// ─── VOTE FLOW ────────────────────────────────────────────────────────────────
let pendingCandidateId = null;

function openVoteModal(candidateId) {
  if (!state.address) { toast("Please connect your wallet first.", "error"); return; }
  if (state.hasVoted) { toast("You have already voted in this election.", "error"); return; }

  const candidate = state.candidates.find(c => Number(c.id) === candidateId);
  if (!candidate) return;

  pendingCandidateId = candidateId;

  els.modalCandidateName.textContent  = candidate.name;
  els.modalCandidateParty.textContent = candidate.party;
  els.modalCandidateId.textContent    = "#" + candidateId;
  els.modalNetwork.textContent        = state.network
    ? state.network.name + " (chainId: " + state.network.chainId + ")"
    : "Demo mode";

  els.voteModal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  els.voteModal.classList.add("hidden");
  document.body.style.overflow = "";
  pendingCandidateId = null;
  resetConfirmBtn();
}

async function submitVote() {
  if (pendingCandidateId === null) return;

  // Demo mode simulation
  if (state.isDemo || !state.contract) {
    simulateDemoVote(pendingCandidateId);
    return;
  }

  setConfirmLoading(true);

  try {
    toast("Sending transaction…", "info");
    const tx = await state.contract.vote(pendingCandidateId);

    addTxLog(tx.hash, "pending", `Voted for candidate #${pendingCandidateId}`);
    toast("Transaction submitted. Waiting for confirmation…", "info");

    const receipt = await tx.wait();

    state.hasVoted  = true;
    state.votedFor  = pendingCandidateId;

    updateTxLog(tx.hash, "vote");
    toast("Vote confirmed! Block #" + receipt.blockNumber, "success");

    closeModal();
    await refreshContractData();

  } catch (err) {
    console.error("Vote failed:", err);

    let msg = "Transaction failed.";
    if (err.code === 4001 || err.code === "ACTION_REJECTED") msg = "Transaction rejected by user.";
    else if (err.reason) msg = err.reason;

    toast(msg, "error");
    if (pendingCandidateId !== null) addTxLog("0x" + Math.random().toString(16).slice(2), "failed", msg);

  } finally {
    setConfirmLoading(false);
  }
}

function simulateDemoVote(candidateId) {
  setConfirmLoading(true);

  setTimeout(() => {
    state.hasVoted = true;
    state.votedFor = candidateId;

    // Update candidate vote count in demo data
    const candidate = state.candidates.find(c => Number(c.id) === candidateId);
    if (candidate) {
      candidate.voteCount = candidate.voteCount + 1n;
      state.electionInfo.totalVotes = (state.electionInfo.totalVotes || 0n) + 1n;
    }

    const fakeTxHash = "0x" + Array.from({length: 64}, () => Math.floor(Math.random()*16).toString(16)).join("");
    addTxLog(fakeTxHash, "vote", `Voted for candidate #${candidateId} (demo)`);

    toast("Demo vote cast! In a real deployment this would be on-chain. 🎉", "success");
    setConfirmLoading(false);
    closeModal();

    updateVoteStatusUI();
    renderCandidates();
    renderResults();
  }, 1500);
}

// ─── UI RENDERING ─────────────────────────────────────────────────────────────

function updateWalletUI() {
  // Header
  els.networkName.textContent = state.network
    ? (state.network.name !== "unknown" ? state.network.name : "Chain " + state.network.chainId)
    : "—";
  els.netDot.classList.add("connected");
  els.connectBtn.textContent = truncateAddress(state.address);

  // Wallet bar
  els.walletBar.classList.remove("hidden");
  els.walletAddress.textContent = state.address;

  // Prompt → candidates
  els.connectPrompt.classList.add("hidden");
  els.candidatesSection.classList.remove("hidden");
  els.resultsSection.classList.remove("hidden");
  els.txSection.classList.remove("hidden");
}

function updateElectionHero() {
  const info = state.electionInfo;
  if (info.title) els.electionTitle.textContent = info.title;

  const chip = els.electionStatus;
  if (info.isOpen) {
    chip.textContent = "● LIVE";
    chip.className   = "meta-value status-chip";
  } else {
    chip.textContent = "● CLOSED";
    chip.className   = "meta-value status-chip closed";
  }

  const tv = info.totalVotes !== undefined ? info.totalVotes : 0n;
  els.totalVotes.textContent = tv.toLocaleString ? tv.toLocaleString() : String(tv);
}

function renderCandidates() {
  const grid = els.candidatesGrid;
  grid.innerHTML = "";

  state.candidates.forEach((c, i) => {
    const id        = Number(c.id);
    const isVoted   = state.hasVoted && state.votedFor === id;
    const isDisabled = state.hasVoted && !isVoted;

    const card = document.createElement("div");
    card.className = `candidate-card${isVoted ? " voted-for" : ""}${isDisabled ? " disabled" : ""}`;
    card.style.animationDelay = `${i * 80}ms`;

    card.innerHTML = `
      <div class="candidate-num">CANDIDATE · ${String(id).padStart(2, "0")}</div>
      <div class="candidate-name">${escHtml(c.name)}</div>
      <div class="candidate-party">${escHtml(c.party)}</div>
      <div class="candidate-manifesto">${escHtml(c.manifesto)}</div>
      <div class="candidate-footer">
        <div class="candidate-votes"><strong>${c.voteCount.toLocaleString ? c.voteCount.toLocaleString() : c.voteCount}</strong> votes</div>
        ${isVoted
          ? `<div class="voted-badge">✓ Your Vote</div>`
          : `<button class="vote-btn" data-id="${id}" ${isDisabled ? "disabled" : ""}>Vote</button>`}
      </div>
    `;

    if (!isDisabled && !isVoted) {
      card.querySelector(".vote-btn")?.addEventListener("click", e => {
        e.stopPropagation();
        openVoteModal(id);
      });
      card.addEventListener("click", () => openVoteModal(id));
    }

    grid.appendChild(card);
  });

  // Show sections
  if (state.address) {
    els.candidatesSection.classList.remove("hidden");
    els.resultsSection.classList.remove("hidden");
  }
}

function renderResults() {
  const container = els.resultsContainer;
  container.innerHTML = "";

  const candidates = [...state.candidates].sort((a, b) =>
    Number(b.voteCount) - Number(a.voteCount)
  );

  const total = candidates.reduce((sum, c) => sum + Number(c.voteCount), 0) || 1;
  const topVotes = Number(candidates[0]?.voteCount ?? 0);

  candidates.forEach((c, i) => {
    const votes  = Number(c.voteCount);
    const pct    = ((votes / total) * 100).toFixed(1);
    const isWinner = votes === topVotes && votes > 0;

    const row = document.createElement("div");
    row.className = `result-row${isWinner ? " winner" : ""}`;
    row.style.animationDelay = `${i * 60}ms`;

    row.innerHTML = `
      <div>
        <div class="result-name">${escHtml(c.name)}${isWinner ? '<span class="winner-crown">👑</span>' : ""}</div>
        <div class="result-party">${escHtml(c.party)}</div>
      </div>
      <div class="result-bar-wrap">
        <div class="result-bar" style="width: ${pct}%"></div>
      </div>
      <div class="result-count">
        <div>${votes.toLocaleString()}</div>
        <div class="result-pct">${pct}%</div>
      </div>
    `;

    container.appendChild(row);
  });
}

function updateVoteStatusUI() {
  if (state.hasVoted) {
    els.voteStatusBadge.classList.add("voted");
    els.voteStatusText.textContent = "Already Voted";
    els.voteStatusBadge.querySelector(".status-dot").style.background = "var(--yellow)";
  } else {
    els.voteStatusBadge.classList.remove("voted");
    els.voteStatusText.textContent = "Eligible to Vote";
  }
}

function checkDemoVoteStatus() {
  // For demo mode, start fresh
  state.hasVoted = false;
  state.votedFor = null;

  // Show candidate section
  els.connectPrompt.classList.add("hidden");
  els.candidatesSection.classList.remove("hidden");
  els.resultsSection.classList.remove("hidden");
  els.txSection.classList.remove("hidden");
  renderCandidates();
  renderResults();
  updateVoteStatusUI();
}

// ─── TRANSACTION LOG ──────────────────────────────────────────────────────────
function addTxLog(hash, type, label) {
  const now   = new Date().toLocaleTimeString();
  const entry = { hash, type, label, time: now };
  state.txLog.unshift(entry);

  // Clear "no txns" message
  const empty = els.txLog.querySelector(".tx-empty");
  if (empty) empty.remove();

  const div = document.createElement("div");
  div.className = "tx-entry";
  div.dataset.hash = hash;
  div.innerHTML = `
    <span class="tx-type ${type}">${type.toUpperCase()}</span>
    <span class="tx-hash">
      <a href="https://etherscan.io/tx/${hash}" target="_blank" rel="noopener">${truncateHash(hash)}</a>
    </span>
    <span class="tx-time">${now}</span>
  `;

  els.txLog.prepend(div);
}

function updateTxLog(hash, newType) {
  const div = els.txLog.querySelector(`[data-hash="${hash}"]`);
  if (div) {
    const chip = div.querySelector(".tx-type");
    if (chip) { chip.textContent = newType.toUpperCase(); chip.className = `tx-type ${newType}`; }
  }
}

// ─── COUNTDOWN ───────────────────────────────────────────────────────────────
function startContractCountdown(endTimestamp) {
  if (state.countdownId) clearInterval(state.countdownId);

  function tick() {
    const remaining = endTimestamp - Math.floor(Date.now() / 1000);
    if (remaining <= 0) {
      els.timeRemaining.textContent = "ENDED";
      clearInterval(state.countdownId);
    } else {
      els.timeRemaining.textContent = formatDuration(remaining);
    }
  }
  tick();
  state.countdownId = setInterval(tick, 1000);
}

function startDemoCountdown() {
  let remaining = 7 * 3600 + 23 * 60 + 44; // demo: 7h 23m 44s
  function tick() {
    if (remaining <= 0) { els.timeRemaining.textContent = "ENDED"; clearInterval(state.countdownId); return; }
    els.timeRemaining.textContent = formatDuration(remaining--);
  }
  tick();
  state.countdownId = setInterval(tick, 1000);
}

function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${String(h).padStart(2,"0")}:${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
}

// ─── CONFIRM BUTTON STATE ────────────────────────────────────────────────────
function setConfirmLoading(loading) {
  els.modalConfirm.disabled = loading;
  els.confirmBtnText.textContent = loading ? "Broadcasting…" : "Cast Vote";
  els.confirmSpinner.classList.toggle("hidden", !loading);
}

function resetConfirmBtn() {
  setConfirmLoading(false);
}

// ─── TOAST ───────────────────────────────────────────────────────────────────
function toast(msg, type = "info") {
  const icons = { success: "✅", error: "❌", info: "ℹ️" };
  const t = document.createElement("div");
  t.className = `toast ${type}`;
  t.innerHTML = `<span class="toast-icon">${icons[type]}</span><span class="toast-msg">${escHtml(msg)}</span>`;
  els.toastContainer.appendChild(t);

  setTimeout(() => {
    t.classList.add("toast-out");
    setTimeout(() => t.remove(), 300);
  }, 4500);
}

// ─── HELPERS ─────────────────────────────────────────────────────────────────
function truncateAddress(addr) {
  if (!addr) return "";
  return addr.slice(0, 6) + "…" + addr.slice(-4);
}

function truncateHash(hash) {
  if (!hash) return "";
  return hash.slice(0, 10) + "…" + hash.slice(-6);
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
