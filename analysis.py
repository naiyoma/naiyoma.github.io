# #!/usr/bin/env python3

# import bz2
# import json
# from pathlib import Path

# def analyze_fingerprint_file(filepath: str):
#     """Analyze a single fingerprint analysis file"""
#     try:
#         with bz2.open(filepath, 'rt') as f:
#             analysis = json.load(f)
            
#         # Print basic information
#         print("\n=== Fingerprint Analysis ===")
#         print(f"Timestamp: {analysis.get('timestamp', 'N/A')}")
#         print(f"Analysis Number: {analysis.get('analysis_number', 'N/A')}")
        
#         # Print node statistics
#         stats = analysis.get('stats', {})
#         print("\nNodes Analyzed:")
#         print(f"  Clearnet Nodes: {stats.get('clearnet_nodes_analyzed', 0)}")
#         print(f"  Tor Nodes: {stats.get('tor_nodes_analyzed', 0)}")
#         print(f"  Total Matches Found: {stats.get('matches_found', 0)}")
        
#         # Print detailed match information
#         matches = analysis.get('matches', [])
#         if matches:
#             print(f"\nDetailed Matches ({len(matches)} total):")
            
#             # Group matches by match ratio for better analysis
#             high_confidence = []
#             medium_confidence = []
#             low_confidence = []
            
#             for match in matches:
#                 analysis_data = match.get('analysis', {})
#                 match_ratio = analysis_data.get('exact_match_ratio', 0)
                
#                 match_info = {
#                     'clearnet': match.get('clearnet_addr'),
#                     'tor': match.get('tor_addr'),
#                     'exact_matches': analysis_data.get('exact_matches', 0),
#                     'ratio': match_ratio,
#                     'details': analysis_data.get('matching_details', [])
#                 }
                
#                 if match_ratio >= 0.8:
#                     high_confidence.append(match_info)
#                 elif match_ratio >= 0.5:
#                     medium_confidence.append(match_info)
#                 else:
#                     low_confidence.append(match_info)
            
#             # Print matches by confidence level
#             print(f"\nHigh Confidence Matches (≥80% overlap): {len(high_confidence)}")
#             for match in high_confidence:
#                 print_match_details(match)
                
#             print(f"\nMedium Confidence Matches (50-79% overlap): {len(medium_confidence)}")
#             for match in medium_confidence:
#                 print_match_details(match)
                
#             print(f"\nLow Confidence Matches (<50% overlap): {len(low_confidence)}")
#             for match in low_confidence:
#                 print_match_details(match)
                
#             # Print summary statistics
#             total_matches = len(matches)
#             ratios = [match.get('analysis', {}).get('exact_match_ratio', 0) for match in matches]
#             avg_ratio = sum(ratios) / len(ratios) if ratios else 0
            
#             print("\nSummary Statistics:")
#             print(f"  Total Matches: {total_matches}")
#             print(f"  Average Match Ratio: {avg_ratio:.3f}")
#             print(f"  High Confidence Matches: {len(high_confidence)} ({len(high_confidence)/total_matches*100:.1f}%)")
#             print(f"  Medium Confidence Matches: {len(medium_confidence)} ({len(medium_confidence)/total_matches*100:.1f}%)")
#             print(f"  Low Confidence Matches: {len(low_confidence)} ({len(low_confidence)/total_matches*100:.1f}%)")
#         else:
#             print("\nNo matches found in this analysis.")
            
#     except Exception as e:
#         print(f"Error analyzing file: {e}")

# def print_match_details(match):
#     """Print detailed information about a single match"""
#     print(f"\nMatch Details:")
#     print(f"  Clearnet Node: {match['clearnet']}")
#     print(f"  Tor Node: {match['tor']}")
#     print(f"  Exact Timestamp Matches: {match['exact_matches']}")
#     print(f"  Match Ratio: {match['ratio']:.3f}")
    
#     if match['details']:
#         print("  Sample of Matching Timestamps:")
#         for detail in match['details'][:2]:  # Show first 2 examples
#             print(f"    Timestamp: {detail.get('timestamp')}")
#             clearnet_peers = detail.get('clearnet_peers', [])
#             tor_peers = detail.get('tor_peers', [])
#             print(f"    Matching Peers: {len(clearnet_peers)} clearnet, {len(tor_peers)} tor")

# if __name__ == "__main__":
#     filepath = "p2p-crawler/results/fingerprint_analysis_2025-01-20T10-12-19Z_1.json.bz2"
#     analyze_fingerprint_file(filepath)


# import json
# import bz2

# # Read the compressed file
# with bz2.open('p2p-crawler/address_collections/tor_responses.json.bz2', 'rt') as f:
#     data = json.load(f)

# # Print summary of data
# print(f"Total clearnet nodes that responded: {len(data)}")

# # Look at responses from each node
# for node_addr, node_data in data.items():
#     print(f"\nNode: {node_addr}")
#     print(f"Response timestamp: {node_data['timestamp']}")
#     print(f"Number of peers reported: {len(node_data['peers'])}")
    
#     # Optional: Look at first few peers this node reported
#     print("Sample of peers:")
#     counter = 0
#     for i, (peer, timestamp) in enumerate(node_data['peers'].items()):
#         # if i >= 5:  # Show only first 5 peers
#         #     break
#         print(f"  {peer}: {timestamp}")
#         counter = counter + 1
#     print(f":number of nodes {counter}")




# import json
# import bz2
# from pathlib import Path
# from datetime import datetime


# def find_exact_timestamp_matches():
#     # Read both files
#     with bz2.open('p2p-crawler/address_collections/clearnet_responses.json.bz2', 'rt') as f:
#         clearnet_data = json.load(f)
#     with bz2.open('p2p-crawler/address_collections/tor_responses.json.bz2', 'rt') as f:
#         tor_data = json.load(f)

#     current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     output_file = f"exact_timestamp_matches_{current_time}.txt"
    
#     with open(output_file, 'w') as f:
#         f.write("Peer-by-Peer Timestamp Match Analysis\n")
#         f.write("===================================\n\n")
#         import pdb; pdb.set_trace()
#         # For each clearnet node
#         for clearnet_addr, clearnet_info in clearnet_data.items():
#             f.write(f"\nAnalyzing clearnet node: {clearnet_addr}\n")
#             clearnet_peers = clearnet_info['peers']
#             f.write(f"Total peers for this node: {len(clearnet_peers)}\n")
            
#             # For each tor node
#             for tor_addr, tor_info in tor_data.items():
#                 matches = 0
#                 tor_peers = tor_info['peers']
                
#                 # Check each address and timestamp in clearnet peers
#                 for address, timestamp in clearnet_peers.items():
#                     # If address exists in tor peers and timestamps match
#                     if address in tor_peers and tor_peers[address] == timestamp:
#                         matches += 1
#                         f.write(f"\nMatch found!\n")
#                         f.write(f"Address: {address}\n")
#                         f.write(f"Timestamp: {timestamp}\n")
                
#                 if matches > 0:
#                     overlap_percentage = (matches / len(clearnet_peers)) * 100
#                     f.write(f"\nTotal matches between {clearnet_addr} and {tor_addr}: {matches}\n")
#                     f.write(f"Overlap percentage: {overlap_percentage:.2f}%\n")
#                     f.write("-" * 50 + "\n")

#         print(f"Analysis complete. Results written to {output_file}")

# # Run the analysis
# find_exact_timestamp_matches()


# import bz2
# import pandas as pd

# # Read the compressed CSV file
# file_path = 'p2p-crawler/result/2025-01-21T13-09-00Z_v3.10.0_reachable_nodes.csv.bz2'
# df = pd.read_csv(bz2.BZ2File(file_path))

# # Display first few rows
# print("\nFirst few rows:")
# print(df.head())

# # Get basic information about the data
# print("\nDataset Info:")
# print(df.info())

# # Get summary statistics
# print("\nSummary Statistics:")
# print(df.describe())

# # Count nodes by network type
# print("\nNodes by network type:")
# print(df['network'].value_counts())







import psycopg2
from datetime import datetime
import logging

class TimestampAnalyzer:
    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%SZ'
        )
        self.log = logging.getLogger(__name__)
        
        self.db_params = {
            'dbname': 'btc_crawler',
            'user': 'btc_crawler_user',
            'password': '1234', 
            'host': 'localhost',
            'port': '5432'
        }
        self.log.info("Initializing TimestampAnalyzer")
        self._initialize_analysis_tables()

    def _initialize_analysis_tables(self):
        self.log.info("Initializing analysis tables")
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()
    
        try:
            self.log.info("Creating analysis_peer_table table if it doesn't exist")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS analysis_peer_table (
                    id SERIAL PRIMARY KEY,
                    analysis_timestamp TIMESTAMP NOT NULL,
                    clearnet_node VARCHAR(255) NOT NULL,
                    clearnet_total_peers INTEGER NOT NULL,
                    tor_node VARCHAR(255) NOT NULL,
                    matched_peer_address VARCHAR(255) NOT NULL,
                    peer_timestamp INTEGER NOT NULL,
                    matches_in_batch INTEGER NOT NULL,
                    overlap_percentage FLOAT NOT NULL
                )
            """)

            self.log.info("Creating log_analysis_2 table if it doesn't exist")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS log_analysis_2 (
                    id SERIAL PRIMARY KEY,
                    analysis_timestamp TIMESTAMP NOT NULL,
                    clearnet_node VARCHAR(255) NOT NULL,
                    message_type VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL
                )
            """)
            
            conn.commit()
            self.log.info("Successfully initialized analysis tables")
        except Exception as e:
            conn.rollback()
            self.log.error(f"Error initializing tables: {e}")
            raise e
        finally:
            cur.close()
            conn.close()

    def analyze_timestamp_matches(self):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()
        try:
            analysis_time = datetime.now()
            batch_size = 100  # Process 100 clearnet nodes at a time
            cur.execute("SELECT DISTINCT node_addr FROM clearnet_responses")
            all_clearnet_nodes = cur.fetchall()
            for i in range(0, len(all_clearnet_nodes), batch_size):
                batch_nodes = all_clearnet_nodes[i:i+batch_size]
                node_list = ",".join([f"'{node[0]}'" for node in batch_nodes])
                cur.execute(f"""
                    WITH matches AS (
                        SELECT 
                            c.node_addr as clearnet_node,
                            t.node_addr as tor_node,
                            c.peer_addr,
                            c.peer_timestamp,
                            COUNT(*) OVER (PARTITION BY c.node_addr, t.node_addr) as batch_count
                        FROM clearnet_responses c
                        JOIN tor_responses t 
                            ON c.peer_addr = t.peer_addr 
                            AND c.peer_timestamp = t.peer_timestamp
                        WHERE c.node_addr IN ({node_list})
                    )
                    INSERT INTO analysis_peer_table (
                        analysis_timestamp, clearnet_node, clearnet_total_peers,
                        tor_node, matched_peer_address, peer_timestamp,
                        matches_in_batch, overlap_percentage
                    )
                    SELECT 
                        %s,
                        m.clearnet_node,
                        COUNT(DISTINCT cr.peer_addr),
                        m.tor_node,
                        m.peer_addr,
                        m.peer_timestamp,
                        m.batch_count,
                        (m.batch_count * 100.0 / COUNT(DISTINCT cr.peer_addr))
                    FROM matches m
                    JOIN clearnet_responses cr ON cr.node_addr = m.clearnet_node
                    GROUP BY m.clearnet_node, m.tor_node, m.peer_addr, m.peer_timestamp, m.batch_count;
                """, (analysis_time,))
                conn.commit()
                self.log.info(f"Processed batch {i//batch_size + 1} of {len(all_clearnet_nodes)//batch_size + 1}")
        finally:
            conn.close()

    def print_latest_analysis(self):
        """Print the latest analysis from both tables"""
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()
        try:
            self.log.info("Retrieving latest analysis results")
            # Get latest timestamp
            cur.execute("""
                SELECT MAX(analysis_timestamp) 
                FROM analysis_peer_table
            """)
            latest_time = cur.fetchone()[0]
            
            if latest_time:
                self.log.info(f"Latest analysis timestamp: {latest_time}")
                
                # Print from analysis_peer_table
                self.log.info("Results from analysis_peer_table table:")
                cur.execute("""
                    SELECT clearnet_node, tor_node, matched_peer_address, peer_timestamp
                    FROM analysis_peer_table 
                    WHERE analysis_timestamp = %s
                    ORDER BY clearnet_node, tor_node
                """, (latest_time,))
                
                results = cur.fetchall()
                import pdb; pdb.set_trace()
                self.log.info(f"Found {len(results)} matches in analysis_peer_table")
                
                # Print from log_analysis_2
                self.log.info("\nResults from log_analysis_2 table:")
                cur.execute("""
                    SELECT message 
                    FROM log_analysis_2 
                    WHERE analysis_timestamp = %s
                    ORDER BY id
                """, (latest_time,))
                
                log_results = cur.fetchall()
                self.log.info(f"Found {len(log_results)} entries in log_analysis_2")
                
                for row in log_results:
                    print(row[0])
            else:
                self.log.warning("No analysis results found in database")
                
        except Exception as e:
            self.log.error(f"Error retrieving analysis: {e}")
            raise e
        finally:
            cur.close()
            conn.close()
            
if __name__ == "__main__":
    try:
        analyzer = TimestampAnalyzer()
        analyzer.analyze_timestamp_matches()
        analyzer.print_latest_analysis()
    except Exception as e:
        logging.error(f"Fatal error in main: {e}")
        raise