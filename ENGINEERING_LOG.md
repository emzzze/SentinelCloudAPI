# ALPHA GUARD IT // ENGINEERING LOG
Proprietor: AlphaGuard IT
--------------------------------

## SESSION: 2026-01-31 01:02
Fuel: Black Coffee & Nicotine
--------------------------------
Completed: Initial architecture of Wrait-Core (AES-256 Vault Logic)
Intergrated: Shadow-Gate authentication (JTW & Bcrypt password hashing)
Security Audit: Logic verified via peer review (Claude AI) to ensure token integrity
Infrastructure: Established WSL-to-macOS sync protocol via custon Bash automation
Goal for tomorrow Implement Audit-Trace for compliance logging
[NOTICE]: System stability higher than developer stability.
[COGNITIVE]: Dizziness detected. Switching from 'Logic' mode to 'Sleep' mode.

## SESSION: 2026-01-31 14:51
Fuel: Black Coffee & Nicotine
--------------------------------
Coffee almost empty let's make another one and get these 10 hours doen today for the login process

## SESSION: 2026-01-31 15:23
Fuel: Black Coffee & Nicotine
--------------------------------

## SESSION: 2026-01-31 19:48
Fuel: Black Coffee & Nicotine
--------------------------------
Fixing gitignore and continuing tomorrow morning. 


## SESSION: 2026-01-31 19:53
Fuel: Black Coffee & Nicotine
--------------------------------

## SESSION: 2026-01-31 19:53
Fuel: Black Coffee & Nicotine
--------------------------------

Infrastructure Challenge: The WSL2/Docker Network Bridge Failure
The Problem: During deployment, the container returned an Unexpected Status: 500 and No Route to Host.

Root Cause Analysis: * Port Locking: A "zombie" process on the Windows host was holding Port 8000, preventing the Docker bridge from binding.

Subnet Conflict: Resetting the Docker daemon caused a DNS desync between the WSL2 virtual adapter and the Windows Host Networking Service (HNS), cutting off internet access for Docker Hub image pulls.

Resolution Strategy:

Network Reset: Force-cleared the Windows HNS and restarted LxssManager to rebuild the virtual switch.

Port Re-mapping: Moved the public-facing API to Port 9000 to bypass the locked host socket.

Hardening Validation: Successfully re-enabled read_only: true and cap_drop: ALL by implementing tmpfs mounts for system-level temporary files, ensuring the app remained functional under a "Zero Trust" filesystem policy.
## SESSION: 2026-02-08 21:00
Fuel: One Beer and some wings
________________________________

Title: The Architecture Pivot – From WSL Bridge Wars to the Intel Tax

1. The Technical Hurdle: Networking Failure (OSI Layer 2)
Context: While developing the Sentinel Security Vault on Windows, I encountered a critical failure in the WSL2 (Windows Subsystem for Linux) network stack.

Symptom: Docker containers lost all external connectivity. A ping 8.8.8.8 failed, and the host was unable to resolve the virtual bridge to the containerized FastAPI backend.

Forensics: The issue was identified at Layer 2 (Data Link) and Layer 3 (Network) of the OSI model. The virtual ethernet (veth) bridge between the Windows Host Network Service (HNS) and the WSL kernel failed to hand off traffic.

Decision: Rather than spending hours "fighting the bridge," I made the architectural decision to pivot to a Unix-native environment (macOS) to ensure a more stable development-to-production parity.

2. The Platform Constraint: OS Version Drift

The Hardware: 2018 Intel Mac running macOS Monterey (12.7.4).

The Problem: Modern Docker Desktop has dropped support for Monterey, requiring macOS Sonoma or later. Attempting a standard install resulted in an "Incompatible Software" error (the dreaded "X" icon).

The Pivot: Switched from the heavyweight Docker Desktop GUI to Colima—a lightweight, open-source container run-time.

The "Intel Tax": Because Monterey binaries are no longer standard for many Homebrew "bottles," I had to compile the entire virtualization stack (QEMU, OpenSSL, CMake) from source. This pushed the CPU to 100% capacity but ensured a "clean" supply chain build.

3. Security & Audit: The "History Scrub"

Incident: Identified a hashed credential file (users.json) that had been committed to the local Git history.

Remediation Plan: Instead of a simple git rm, I am implementing a full history purge using git-filter-repo.

Learning: This reinforces the "Zero Trust" model—never trust your own history if it was once unencrypted.

4. Current Status

Infrastructure: Colima installation in progress (Compiling QEMU).

Next Milestone: Finalizing the "Hardened" Dockerfile (non-root users, multi-stage builds) and performing a fresh Git push from the new Mac environment.

