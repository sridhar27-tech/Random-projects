// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title Voting
 * @dev A decentralized voting smart contract
 * @notice Each address can vote only once. Admin manages candidates and voting periods.
 */
contract Voting {
    // ─── State Variables ────────────────────────────────────────────────────────

    address public admin;
    string  public electionTitle;
    bool    public votingOpen;
    uint256 public votingStart;
    uint256 public votingEnd;
    uint256 public totalVotes;

    // ─── Structs ────────────────────────────────────────────────────────────────

    struct Candidate {
        uint256 id;
        string  name;
        string  party;
        string  manifesto;
        uint256 voteCount;
        bool    exists;
    }

    // ─── Mappings ───────────────────────────────────────────────────────────────

    mapping(uint256 => Candidate) public candidates;
    mapping(address => bool)      public hasVoted;
    mapping(address => uint256)   public voterChoice;

    uint256 public candidateCount;

    // ─── Events ─────────────────────────────────────────────────────────────────

    event VoteCast(address indexed voter, uint256 indexed candidateId, uint256 timestamp);
    event CandidateAdded(uint256 indexed candidateId, string name, string party);
    event VotingStarted(uint256 startTime, uint256 endTime);
    event VotingEnded(uint256 endTime, uint256 totalVotes);

    // ─── Modifiers ──────────────────────────────────────────────────────────────

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    modifier whenVotingOpen() {
        require(votingOpen, "Voting is not currently open");
        require(block.timestamp >= votingStart, "Voting has not started yet");
        require(block.timestamp <= votingEnd, "Voting period has ended");
        _;
    }

    modifier hasNotVoted() {
        require(!hasVoted[msg.sender], "You have already cast your vote");
        _;
    }

    // ─── Constructor ────────────────────────────────────────────────────────────

    constructor(string memory _electionTitle) {
        admin         = msg.sender;
        electionTitle = _electionTitle;
        votingOpen    = false;
    }

    // ─── Admin Functions ────────────────────────────────────────────────────────

    /**
     * @dev Add a candidate to the election
     * @param _name      Candidate's full name
     * @param _party     Political party or group
     * @param _manifesto Short description / manifesto
     */
    function addCandidate(
        string memory _name,
        string memory _party,
        string memory _manifesto
    ) external onlyAdmin {
        require(!votingOpen, "Cannot add candidates during active voting");
        require(bytes(_name).length > 0, "Candidate name cannot be empty");

        candidateCount++;
        candidates[candidateCount] = Candidate({
            id:        candidateCount,
            name:      _name,
            party:     _party,
            manifesto: _manifesto,
            voteCount: 0,
            exists:    true
        });

        emit CandidateAdded(candidateCount, _name, _party);
    }

    /**
     * @dev Open the voting period
     * @param _durationMinutes Duration of voting in minutes
     */
    function startVoting(uint256 _durationMinutes) external onlyAdmin {
        require(!votingOpen, "Voting is already open");
        require(candidateCount >= 2, "Need at least 2 candidates");
        require(_durationMinutes > 0, "Duration must be positive");

        votingOpen  = true;
        votingStart = block.timestamp;
        votingEnd   = block.timestamp + (_durationMinutes * 60);

        emit VotingStarted(votingStart, votingEnd);
    }

    /**
     * @dev Manually close voting before time expires
     */
    function endVoting() external onlyAdmin {
        require(votingOpen, "Voting is not open");
        votingOpen = false;
        emit VotingEnded(block.timestamp, totalVotes);
    }

    // ─── Voter Functions ─────────────────────────────────────────────────────────

    /**
     * @dev Cast a vote for a candidate
     * @param _candidateId ID of the candidate to vote for
     */
    function vote(uint256 _candidateId) external whenVotingOpen hasNotVoted {
        require(candidates[_candidateId].exists, "Candidate does not exist");

        hasVoted[msg.sender]    = true;
        voterChoice[msg.sender] = _candidateId;

        candidates[_candidateId].voteCount++;
        totalVotes++;

        emit VoteCast(msg.sender, _candidateId, block.timestamp);
    }

    // ─── View Functions ──────────────────────────────────────────────────────────

    /**
     * @dev Get all candidates with their vote counts
     */
    function getAllCandidates() external view returns (Candidate[] memory) {
        Candidate[] memory allCandidates = new Candidate[](candidateCount);
        for (uint256 i = 1; i <= candidateCount; i++) {
            allCandidates[i - 1] = candidates[i];
        }
        return allCandidates;
    }

    /**
     * @dev Get the current winner (candidate with most votes)
     */
    function getWinner() external view returns (Candidate memory winner) {
        require(candidateCount > 0, "No candidates registered");
        uint256 maxVotes = 0;
        for (uint256 i = 1; i <= candidateCount; i++) {
            if (candidates[i].voteCount > maxVotes) {
                maxVotes = candidates[i].voteCount;
                winner   = candidates[i];
            }
        }
    }

    /**
     * @dev Get remaining voting time in seconds
     */
    function getRemainingTime() external view returns (uint256) {
        if (!votingOpen || block.timestamp > votingEnd) return 0;
        return votingEnd - block.timestamp;
    }

    /**
     * @dev Get election status summary
     */
    function getElectionInfo() external view returns (
        string memory title,
        bool          isOpen,
        uint256       start,
        uint256       end,
        uint256       votes,
        uint256       numCandidates,
        address       adminAddr
    ) {
        return (
            electionTitle,
            votingOpen,
            votingStart,
            votingEnd,
            totalVotes,
            candidateCount,
            admin
        );
    }
}
