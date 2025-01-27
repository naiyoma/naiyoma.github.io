



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