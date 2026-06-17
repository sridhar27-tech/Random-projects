const { expect }       = require("chai");
const { ethers }       = require("hardhat");
const { loadFixture }  = require("@nomicfoundation/hardhat-toolbox/network-helpers");

describe("Voting Contract", function () {

  // ─── FIXTURE ──────────────────────────────────────────────────────────────
  async function deployVotingFixture() {
    const [admin, voter1, voter2, voter3] = await ethers.getSigners();

    const Voting = await ethers.getContractFactory("Voting");
    const voting = await Voting.deploy("Test Election 2024");

    // Add 2 candidates
    await voting.addCandidate("Alice Johnson", "Party A", "Better future for all");
    await voting.addCandidate("Bob Smith",     "Party B", "Strong economy first");

    return { voting, admin, voter1, voter2, voter3 };
  }

  async function deployAndStartFixture() {
    const ctx = await deployVotingFixture();
    await ctx.voting.startVoting(60); // 60 minute election
    return ctx;
  }

  // ─── DEPLOYMENT ───────────────────────────────────────────────────────────
  describe("Deployment", function () {
    it("Should set the correct admin", async function () {
      const { voting, admin } = await loadFixture(deployVotingFixture);
      expect(await voting.admin()).to.equal(admin.address);
    });

    it("Should set the correct election title", async function () {
      const { voting } = await loadFixture(deployVotingFixture);
      expect(await voting.electionTitle()).to.equal("Test Election 2024");
    });

    it("Should start with voting closed", async function () {
      const { voting } = await loadFixture(deployVotingFixture);
      expect(await voting.votingOpen()).to.equal(false);
    });
  });

  // ─── CANDIDATES ───────────────────────────────────────────────────────────
  describe("Candidates", function () {
    it("Should add candidates correctly", async function () {
      const { voting } = await loadFixture(deployVotingFixture);
      expect(await voting.candidateCount()).to.equal(2);

      const c = await voting.candidates(1);
      expect(c.name).to.equal("Alice Johnson");
      expect(c.party).to.equal("Party A");
      expect(c.voteCount).to.equal(0);
    });

    it("Should get all candidates", async function () {
      const { voting } = await loadFixture(deployVotingFixture);
      const all = await voting.getAllCandidates();
      expect(all.length).to.equal(2);
    });

    it("Should not allow adding candidates during voting", async function () {
      const { voting } = await loadFixture(deployAndStartFixture);
      await expect(
        voting.addCandidate("Charlie", "Party C", "Change everything")
      ).to.be.revertedWith("Cannot add candidates during active voting");
    });

    it("Should not allow non-admin to add candidates", async function () {
      const { voting, voter1 } = await loadFixture(deployVotingFixture);
      await expect(
        voting.connect(voter1).addCandidate("Charlie", "Party C", "xyz")
      ).to.be.revertedWith("Only admin can call this function");
    });
  });

  // ─── VOTING ───────────────────────────────────────────────────────────────
  describe("Voting", function () {
    it("Should allow a voter to cast a vote", async function () {
      const { voting, voter1 } = await loadFixture(deployAndStartFixture);

      await expect(voting.connect(voter1).vote(1))
        .to.emit(voting, "VoteCast")
        .withArgs(voter1.address, 1, await getCurrentTimestamp());

      expect(await voting.hasVoted(voter1.address)).to.equal(true);
      expect(await voting.voterChoice(voter1.address)).to.equal(1);
      expect(await voting.totalVotes()).to.equal(1);
    });

    it("Should not allow double voting", async function () {
      const { voting, voter1 } = await loadFixture(deployAndStartFixture);

      await voting.connect(voter1).vote(1);
      await expect(
        voting.connect(voter1).vote(2)
      ).to.be.revertedWith("You have already cast your vote");
    });

    it("Should not allow voting for non-existent candidate", async function () {
      const { voting, voter1 } = await loadFixture(deployAndStartFixture);
      await expect(
        voting.connect(voter1).vote(99)
      ).to.be.revertedWith("Candidate does not exist");
    });

    it("Should not allow voting when voting is closed", async function () {
      const { voting, voter1 } = await loadFixture(deployVotingFixture);
      await expect(
        voting.connect(voter1).vote(1)
      ).to.be.revertedWith("Voting is not currently open");
    });

    it("Should correctly tally votes from multiple voters", async function () {
      const { voting, voter1, voter2, voter3 } = await loadFixture(deployAndStartFixture);

      await voting.connect(voter1).vote(1);
      await voting.connect(voter2).vote(1);
      await voting.connect(voter3).vote(2);

      expect(await voting.totalVotes()).to.equal(3);

      const c1 = await voting.candidates(1);
      const c2 = await voting.candidates(2);
      expect(c1.voteCount).to.equal(2);
      expect(c2.voteCount).to.equal(1);
    });

    it("Should identify the winner correctly", async function () {
      const { voting, voter1, voter2, voter3 } = await loadFixture(deployAndStartFixture);

      await voting.connect(voter1).vote(2);
      await voting.connect(voter2).vote(2);
      await voting.connect(voter3).vote(1);

      const winner = await voting.getWinner();
      expect(winner.name).to.equal("Bob Smith");
      expect(winner.voteCount).to.equal(2);
    });
  });

  // ─── ADMIN ────────────────────────────────────────────────────────────────
  describe("Admin Controls", function () {
    it("Should start voting correctly", async function () {
      const { voting } = await loadFixture(deployVotingFixture);
      await expect(voting.startVoting(60))
        .to.emit(voting, "VotingStarted");

      expect(await voting.votingOpen()).to.equal(true);
    });

    it("Should not start voting with less than 2 candidates", async function () {
      const [admin] = await ethers.getSigners();
      const Voting = await ethers.getContractFactory("Voting");
      const fresh = await Voting.deploy("One Candidate Election");
      await fresh.addCandidate("Solo Candidate", "No Party", "Only me");

      await expect(fresh.startVoting(60)).to.be.revertedWith(
        "Need at least 2 candidates"
      );
    });

    it("Should allow admin to end voting early", async function () {
      const { voting } = await loadFixture(deployAndStartFixture);
      await expect(voting.endVoting())
        .to.emit(voting, "VotingEnded");

      expect(await voting.votingOpen()).to.equal(false);
    });

    it("Should not allow non-admin to start or end voting", async function () {
      const { voting, voter1 } = await loadFixture(deployVotingFixture);

      await expect(
        voting.connect(voter1).startVoting(60)
      ).to.be.revertedWith("Only admin can call this function");
    });
  });

  // ─── HELPER ───────────────────────────────────────────────────────────────
  async function getCurrentTimestamp() {
    const block = await ethers.provider.getBlock("latest");
    return block.timestamp + 1; // approximate
  }
});
