import streamlit as st
import subprocess
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Function to check ping status using ICMP
def check_ping(host):
    """Checks if a host is reachable via ICMP ping."""
    try:
        # Use the 'ping' command with ICMP option (if available)
        if os.name == 'nt':  # Windows
            output = subprocess.check_output(["ping", "-n", "1", host], shell=True, text=True)
        else:  # Linux/macOS
            output = subprocess.check_output(["ping", "-c", "1", host], shell=True, text=True)

        # Check for success message in the output (message varies by OS)
        if "Reply from" in output or "1 packets transmitted, 1 received" in output:
            return True
        else:
            return False

    except subprocess.CalledProcessError:
        return False

# Streamlit app
def main():
    st.set_page_config(layout="wide", page_title="Network Operations Centre by Yash", page_icon="📡")
    st.header("Network Operations Centre V.0.0.1 by Yash Kulkarni")
    st.text("This Project is solely undertaken by me for personal use and this tool was developed using Python 3.13")

    # Theme toggle
    theme_mode = st.radio("Theme", ["Dark", "Light"])
    if theme_mode == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #222;
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #fff;
            }
            </style>
            """, unsafe_allow_html=True)

    # Create columns for panels
    col1, col2, col3 = st.columns(3)

    # Server input and add button (Panel 1)
    with col1:
        st.header("Server Input")
        server_list = st.text_input("Enter server addresses (Hostname / IP)", "")

        if st.button("Add Servers"):
            if server_list:
                servers = server_list.split(",")
                for server in servers:
                    if server not in st.session_state.get('servers', []):
                        st.session_state.servers = st.session_state.get('servers', []) + [server]

                        # Initialize ping history and uptime data for the new server
                        if 'ping_history' not in st.session_state:
                            st.session_state.ping_history = {}
                        st.session_state.ping_history[server] = []
                        if 'uptime_data' not in st.session_state:
                            st.session_state.uptime_data = {}
                        st.session_state.uptime_data[server] = {'up_time': 0, 'down_time': 0, 'last_status': None, 'last_status_change': None}

    # KPI Panel (Panel 2)
    with col2:
        st.header("Key Performance Indicators")
        if st.session_state.get('servers'):
            server_count = len(st.session_state.get('servers'))
            server_up = 0
            server_down = 0

            for server in st.session_state.servers:
                if check_ping(server):
                    server_up += 1
                else:
                    server_down = server_count - server_up

            # Display KPIs with live updates
            col21, col22 = st.columns(2)
            with col21:
                st.metric("Total Servers", server_count)
                st.metric("Servers Up", server_up)
            with col22:
                st.metric("Servers Down", server_down)

    # Server Status Panel (Panel 3)
    with col3:
        st.header("Server Status")
        if st.session_state.get('servers'):
            status_df = pd.DataFrame({'Server': st.session_state.servers})
            status_df['Status'] = status_df['Server'].apply(lambda x: "UP" if check_ping(x) else "DOWN")
            st.table(status_df)

    # Ping History Chart (Panel 1)
    with col1:
        st.header("Ping History")
        if st.session_state.get('servers'):
            if 'ping_history_df' not in st.session_state:
                st.session_state.ping_history_df = pd.DataFrame(columns=st.session_state.get('servers', []))

            # Update ping history every second
            if st.session_state.get('servers'):
                for server in st.session_state.servers:
                    try:
                        result = subprocess.run(["ping", "-c", "1", server], stdout=subprocess.DEVNULL, timeout=1)
                        if result.returncode == 0:
                            st.session_state.ping_history[server].append(0)  # Record successful ping as 0 ms latency
                        else:
                            st.session_state.ping_history[server].append(1000)  # Record failed ping as 1000 ms latency
                    except subprocess.TimeoutExpired:
                        st.session_state.ping_history[server].append(1000)  # Record timeout as 1000 ms latency

                # Update DataFrame with new ping history data
                for server in st.session_state.servers:
                    if len(st.session_state.ping_history[server]) > 0:
                        st.session_state.ping_history_df.loc[len(st.session_state.ping_history_df)] = {server: st.session_state.ping_history[server][-1]}

                # Create line chart
                if not st.session_state.ping_history_df.empty:
                    fig, ax = plt.subplots()
                    sns.lineplot(data=st.session_state.ping_history_df, ax=ax)
                    ax.set_ylabel("Ping Latency (ms)")
                    st.pyplot(fig)

    # Server Status Distribution (Panel 2)
    with col2:
        st.header("Server Status Distribution")
        if st.session_state.get('servers'):
            status_counts = status_df['Status'].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=status_counts.index, y=status_counts, ax=ax)
            ax.set_ylabel("Number of Servers")
            st.pyplot(fig)

    # Server Uptime/Downtime (Panel 3)
    with col3:
        st.header("Server Uptime/Downtime")
        if st.session_state.get('servers'):
            for server in st.session_state.servers:
                current_status = check_ping(server)
                if current_status != st.session_state.uptime_data[server]['last_status']:
                    if current_status:  # Server is up
                        st.session_state.uptime_data[server]['last_status_change'] = datetime.datetime.now()
                    else:  # Server is down
                        if st.session_state.uptime_data[server]['last_status']:  # If previously up, calculate downtime
                            downtime = datetime.datetime.now() - st.session_state.uptime_data[server]['last_status_change']
                            st.session_state.uptime_data[server]['down_time'] += downtime.total_seconds()

                st.session_state.uptime_data[server]['last_status'] = current_status

            for server in st.session_state.servers:
                uptime_str = str(datetime.timedelta(seconds=st.session_state.uptime_data[server]['up_time']))
                downtime_str = str(datetime.timedelta(seconds=st.session_state.uptime_data[server]['down_time']))
                st.write(f"**{server}**: Uptime: {uptime_str}, Downtime: {downtime_str}")

    # Add a refresh button
    if st.button("Refresh"):
        st.cache

if __name__ == "__main__":
    main()