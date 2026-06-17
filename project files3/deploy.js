 
const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contract with account:", deployer.address);

  const ELECTION_TITLE = "2024 Community Leadership Election";
  const Voting = await ethers.getContractFactory("Voting");
  const voting = await Voting.deploy(ELECTION_TITLE);
  await voting.waitForDeployment();

  const address = await voting.getAddress();
  console.log("\n✅ Voting contract deployed to:", address);

  console.log("\nAdding candidates...");

  const candidates = [
    {
      name:      "Alexandra Reyes",
      party:     "Progressive Alliance",
      manifesto: "Championing renewable energy, universal healthcare, and a living wage for all citizens.",
    },
    {
      name:      "Marcus Bennett",
      party:     "Liberty First",
      manifesto: "Lower taxes, deregulation, and strong border security to restore economic freedom.",
    },
    {
      name:      "Priya Sharma",
      party:     "Future Forward",
      manifesto: "Technology-driven governance, open innovation, and evidence-based policy for the digital age.",
    },
    {
      name:      "Daniel Okafor",
      party:     "Community Coalition",
      manifesto: "Grassroots democracy, community ownership, and rebuilding trust between citizens and institutions.",
    },
  ];

  for (const c of candidates) {
    const tx = await voting.addCandidate(c.name, c.party, c.manifesto);
    await tx.wait();
    console.log(`   ✓ Added candidate: ${c.name}`);
  }

  console.log("\nStarting voting period (120 minutes)...");
  const startTx = await voting.startVoting(120);
  await startTx.wait();
  console.log("   ✓ Voting is now OPEN");

  console.log("\n═══════════════════════════════════════");
  console.log("  CONTRACT ADDRESS:", address);
  console.log("  Copy this into app.js → CONTRACT_ADDRESS");
  console.log("═══════════════════════════════════════\n");
}

main()
  .then(() => process.exit(0))
  .catch(err => {
    console.error(err);
    process.exit(1);
  });