---
title: Network Path Analysis - Evolving Network Diagnostics for the Modern Security Landscape
date: 2025-02-19
tags: networking, laboratory, ping, traceroute
description: 
---

## Abstract


## Introduction

In today's networks, security isn't just an added feature; it's the foundational architecture. Modern networks are increasingly hardened, employing sophisticated firewalls, intrusion detection systems, and traffic filtering policies. While essential for protecting against threats, these security measures significantly impact the effectiveness of traditional network diagnostic tools like `ping`, `traceroute`, and even basic DNS queries using tools like `dig`.  These classic utilities, which heavily rely on the Internet Control Message Protocol (ICMP) and simple UDP probes, often find themselves blocked or rate-limited in security-conscious environments, leaving network administrators and security professionals with a diminished ability to diagnose and troubleshoot effectively.

This blog post modernizes our approach to network diagnostics by introducing a suite of advanced tools designed to navigate the challenges of security-hardened networks.  We move beyond the limitations of ICMP-centric utilities and embrace tools that leverage TCP, UDP, and application-layer protocols to gain deeper insights into network behavior. This updated methodology not only ensures continued diagnostic capability but also provides a more accurate representation of network performance as experienced by modern applications and users.

In this experiment, we will explore kdig for advanced DNS analysis, hping3 for flexible connectivity and latency testing, tcptraceroute for path discovery through firewalls, and nping for comprehensive network probing and analysis.  These tools represent a significant evolution in network diagnostics, offering robust capabilities for understanding network behavior in the face of modern security implementations.  By mastering these techniques, network professionals can regain visibility and control, ensuring network reliability and performance even in the most rigorously secured environments.

### Key Concepts and Definitions:


### Network Diagnostic Tools


### Objectives


## Experimental

Using a 2.6 GHz 6-Core Intel Core i7 MacBook Pro with 16 GB 2667 MHz DDR4 RAM running macOS Sequoia 15.3.1 and built in Wi-Fi run following terminal commands. All commands are non-intrusive network diagnostics. Some commands require administrator privileges (sudo). Rate limiting is built into tools to prevent network flooding. All targets are public services designed to handle routine diagnostics.

1. Advanced DNS Resolution Analysis with kdig:
```zsh
# Basic A record lookup and query timing
kdig +stats level3.net
```

```zsh
# Explore CNAME chain resolution
kdig +trace aws.amazon.com
```
```zsh
# DNSSEC validation check
kdig +dnssec aws.amazon.com
```

```zsh
# Query specific record types (e.g., MX records for email servers)
kdig MX gmail.com
```

2. Flexible Connectivity and Latency Testing with hping3:
```zsh
# TCP SYN ping to port 80 (HTTP)
sudo hping3 -S -p 80 -c 5 aws.amazon.com
```

```zsh
# TCP SYN ping to port 443 (HTTPS) with smaller packet size (testing a possible MTU effect in TCP)
sudo hping3 -S -p 443 -c 5 -d 1400 aws.amazon.com
```

```zsh
# UDP ping (for comparison, even if often filtered, might reveal something)
sudo hping3 -2 -c 5 aws.amazon.com
```

3. Firewall-Penetrating Path Analysis with tcptraceroute:
```zsh
# TCP traceroute to port 80
sudo tcptraceroute -n -p 80 aws.amazon.com
```
```zsh
# TCP traceroute to port 443
sudo tcptraceroute -n -p 443 aws.amazon.com
```
```zsh
# Compare with standard traceroute (for reference and to highlight differences)
traceroute -n aws.amazon.com
```

4. Comprehensive Network Probing with nping:
```zsh
# TCP SYN scan and timing to port 80
sudo nping --tcp-syn -p 80 --count 5 --delay 100ms aws.amazon.com
```
```zsh
# UDP probe and timing
sudo nping --udp -p 53 --count 5 --delay 100ms aws.amazon.com
```
```zsh
# ICMP probe and timing (for comparison)
sudo nping --icmp --ping --count 5 --delay 100ms aws.amazon.com
```
```zsh
# TCP Traceroute-like path discovery with nping (using TCP SYN)
sudo nping --tcp-syn --traceroute -p 80 aws.amazon.com
```

## Results

## Discussion

### Conclusion

### References