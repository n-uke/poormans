import subprocess
import json
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

DATA_FOLDER="epoch_data"

# Dictionary mapping addresses to Discord handles
address_to_discord = {
    "0x86554d60d94378e32ee3ec053d8e32c3f1b37725a73a95f084381edfc1e76354": "@.m0ot",
    "0xc88f9adcb4c0678b9475e79355c53bb4": "@.n.u.k.e.",
    "0x79784b5981cc5407ba3bf9f7526f3f54": "@_easy123",
    "0xaa7b724a51a8bd8e55208fef969209b3": "@0xslipk",
    "0xd19a9e5149ab0038f3563caf6b3e7063dca5bfe9dc37cb7f7194806ceaa4f5c4": "@0xslipk",
    "0xc80696fa9d3d161261246d3fdbfd982402856dfe22ffc571b80c3acc67c2bda4": "@0xslipk",
    "0xca6bf512e1ca96ed2a6ef5b74bb8ba5daca689e8b314c4414440ebeb5b82fdf2": "@aaronwhite9527",
    "0x56641e58aba97fa6b7ea833f83444392": "@abed8998",
    "0xc0de6c80d94060c89dcb3e47c43faf3d7a2f070a51faeab0fb46ac8041f6425d": "@badrock42 (Adal)",
    "0x32f24e0488a4e189d38fccd1f2a94b53": "@alanyoon.1",
    "0xab8071fddaacc1a48ca6901d87ad3d181f8bd344bc8defee1bc353cb26f2cefe": "@alanyoon.2",
    "0x8186f4d8fdd09dfe02963b0b4c385105": "@ashiiix",
    "0x9499c45e34ef05a9afd295779d989cbafaf973dbcdd35a9ae6be5fa8afa9861f": "@barmaley8971",
    "0x95c872c5519a0e165886b4e752f23b545805a218e50f0e846f5976ea3b026ae5": "@bbk8530.1",
    "0xd578395a5a130fcd0ff13ed6a1c5af37": "@bbk8530.2",
    "0x754903132f75c0b1f5e5be29fb0ca6cd": "@bethose",
    "0x949ea6affb7a4b43f157158319b5d51c": "@bigbubabeast",
    "0xb32e1c7b70c711d7992fee1219ecaa50dfd2cfe9283b68e2ae6aff1c990f80dd": "@blackgrouse_.1",
    "0xf2103cc8b36205aed79c8e5a441fc4e75af07d5e33325491f08a98f604b5fd78": "@blackgrouse_.2",
    "0x13a65b0c9500848a6e8cc9a8c45e2c0750f6860fe9aad7e956e27de10956dddd": "@c64michael",
    "0x9a01290c3ab972597a71194428318cd87361fe41ce9a451eebfe8d3748377a2e": "@coin1111",
    "0x1fffe941a07d96a181a30934c9dbece13f1f6ae7df3af40203ecd31dba80ecd9": "@dboreham",
    "0xb8ba6c084fa504add5f23ae51e41f23d": "@dmski1",
    "0x77f2650cd59335a8b03f875b43376f26": "@hemulin",
    "0xb295da228c6808199d92dc813975755c": "@imstar15",
    "0x2fa553d9ab2d5e0bf39bf9147b61a5d0fd78ebe7256ace2c9470020fbbea95a0": "@johnpaul9185.1",
    "0xb1ebce2a604d0d277ff1b5f9ea7a4e8a8370c8f487edea5d7df85448b828cfd6": "@johnpaul9185.2",
    "0x16b3da73e53d17bfeb6b542f1ac33444": "@judasdaygame",
    "0xcf18bf38fe71080c3c199868ed167693": "@kalvinen",
    "0xfdcf0ef094b962fb35997f4e2bcd4f27533b567bf8518f5b4f9400f47742be9b": "@lemonium9962",
    "0x52d79701968e2ab8d34ddd77ad11e87f": "@luckyduder",
    "0x71e5be86b41516743ac8594bc90ee2fc": "@mrrob0t333", 
    "0d78...5a1a": "@ncontrol88", 
    "0xe77ddb76c9afcb3d5511e46cbc89023d": "@nourspace", 
    "0x4edef1a648ce28eaa71e3d6eb205a0f9c668bb7f025e6d3de4e133657fdd093a": "@ownyrd",
    "0xb3848a1353f194692551661fe43933b4af80f92e75e9ecc2d2b08e4ca970e0d8": "@pedro00",
    "0x9909f6edb2a0684adecd7b448b989e4f": "@pithecus.astr",
    "0x6122b508960bbdbbf28f38bc035c393ecf7cff54c3ce8282c735940eedd807a": "@qusuy", 
    "0xb5b5ba58b8e9916fe449d1f989383834": "@ricoflan",
    "0x4d250de8388d8232f702ffc6de74df626325cbd24ad416350ab2a4e30b2c92c6": "@saturn_0505",
    "0x9a710919b1a1e67eda335269c0085c91": "@sirouk",
    "0xf48513d19e39488b20ff63a798affa544d45db9aca5e544fdd2e8b6e4a4c017e": "@slappymcslapper",
    "0x25c39d475e12cd20623b75d33046baa442b8115c80fea816bf0198954ae9e341": "@texaseduc8r",
    "0x744185aebd902421992147559f35eb937058ac74116fd6d1d6bc93ab95805aea": "@tabletoptawny",
    "0x2023c65e5323feb2671eb690d5649ae3": "@theoneid",
    "0x9763a662ac509b8e6aae78aa628cbf46569a46e6e94b080c35e44d28368ee0ea": "@w3sc",
    "0x55b6ba3408f670418371f500b9f431dc0e867f09974812b32c6d3a614d35cca6": "@wuya51",
    "0x9de57cf5f154889bd4bdfb286fe1aedc7f58e7640f14dbe5f12cfff43255be48": "@zerooooooooo1",
}

def save_current_run(qualified_bidders, auction_winners, bids, vouches, balances, jail_info, pof_info, filepath):
    data = {
        "qualified_bidders": qualified_bidders,
        "auction_winners": auction_winners,
        "bids": bids,
        "vouches": vouches,
        "balances": balances,
        "jail_info": jail_info,
        "pof_info": pof_info
    }
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_previous_run(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {"qualified_bidders": [], "auction_winners": [], "bids": {}, "vouches": {}, "balances": {}, "jail_info": {}, "pof_info": {}}

def compare_runs(current_bidders, current_winners, current_bids, current_vouches, current_balances, current_jail_info, previous_bidders, previous_winners, previous_bids, previous_vouches, previous_balances, previous_jail_info, epoch_number, set_size, pof_info, previous_pof_info, file_path):
    def format_balances_with_changes(current, previous):
        total = current.get("total_balance", 0)
        unlocked = current.get("unlocked_balance", 0)
        locked = current.get("locked_balance", 0)

        # Calculate the changes between current and previous balances
        total_change = total - previous.get("total_balance", 0)
        unlocked_change = unlocked - previous.get("unlocked_balance", 0)
        locked_change = locked - previous.get("locked_balance", 0)

        # Format the balances and changes
        return (
            f"{total:,.2f} ({total_change:+,.2f})",
            f"{unlocked:,.2f} ({unlocked_change:+,.2f})",
            f"{locked:,.2f} ({locked_change:+,.2f})"
        )

    
    def format_bid_with_changes(current_bid, previous_bid):
        if previous_bid is not None:
            bid_change = current_bid - previous_bid
            if bid_change != 0:  # Only print if change is not 0
                return f"{current_bid:,.2f} ({bid_change:+,.2f})"
        return f"{current_bid:,.2f}"

    # Determine the maximum width needed for each column
    # Determine the maximum width needed for each column
    def calculate_max_widths(entries, balances, bids):
        max_total_width = 0
        max_unlocked_width = 0
        max_locked_width = 0
        max_bid_width = 0

        for addr in entries:
            # Format bid with changes
            current_bid = bids.get(addr, 0)
            previous_bid = previous_bids.get(addr, 0)
            formatted_bid = format_bid_with_changes(current_bid, previous_bid)
            max_bid_width = max(max_bid_width, len(formatted_bid))
            

            # Format balances
            current_balance = balances.get(addr, {"total_balance": 0, "unlocked_balance": 0, "locked_balance": 0})
            prev_balance = previous_balances.get(addr, {"total_balance": 0, "unlocked_balance": 0, "locked_balance": 0})
            formatted_balance = format_balances_with_changes(current_balance, prev_balance)
            total_width = len(formatted_balance[0])
            unlocked_width = len(formatted_balance[1])
            locked_width = len(formatted_balance[2])

            max_total_width = max(max_total_width, total_width)
            max_unlocked_width = max(max_unlocked_width, unlocked_width)
            max_locked_width = max(max_locked_width, locked_width)

        return max_bid_width, max_total_width, max_unlocked_width, max_locked_width

    # Compute max widths for bids and balances
    max_bid_width, max_total_width, max_unlocked_width, max_locked_width = calculate_max_widths(current_bidders + current_winners, current_balances, current_bids)

    # Define fixed widths for columns
    addr_width = 15
    handle_width = 20
    bid_width = max_bid_width + 2  # Add some padding
    total_width = max_total_width + 2  # Add some padding
    unlocked_width = max_unlocked_width + 2
    locked_width = max_locked_width + 2

    header_format = "{:<{addr_width}} {:<{handle_width}} {:<{bid_width}} {:<{total_width}} {:<{unlocked_width}} {:<{locked_width}}\n".format
    row_format = "{:<{addr_width}} {:<{handle_width}} {:<{bid_width}} {:<{total_width}} {:<{unlocked_width}} {:<{locked_width}}\n".format


    dropped_bidders = set(previous_bidders) - set(current_bidders)
    added_bidders = set(current_bidders) - set(previous_bidders)
    dropped_winners = set(previous_winners) - set(current_winners)
    added_winners = set(current_winners) - set(previous_winners)
    changed_bids = {address: current_bids[address] for address in current_bids 
                    if address in previous_bids and current_bids[address] != previous_bids[address]}

    # Ensure epoch_number is an integer
    epoch_number = int(epoch_number)

    # Split vouches into received and given
    current_received_vouches = {addr: vouches.get("received_vouches", {}) for addr, vouches in current_vouches.items()}
    current_given_vouches = {addr: vouches.get("given_vouches", {}) for addr, vouches in current_vouches.items()}
    previous_received_vouches = {addr: vouches.get("received_vouches", {}) for addr, vouches in previous_vouches.items()}
    previous_given_vouches = {addr: vouches.get("given_vouches", {}) for addr, vouches in previous_vouches.items()}

    # Detect changes in received vouches
    changed_received_vouches = {}
    for address in current_received_vouches:
        if address in previous_received_vouches:
            previous_vouches = previous_received_vouches[address]
            current_vouches = current_received_vouches[address]
            added_vouches = [vouch for vouch in current_vouches if vouch not in previous_vouches]
            removed_vouches = [vouch for vouch in previous_vouches if vouch not in current_vouches]
            expired_vouches = [vouch for vouch, vouch_epoch in previous_vouches.items()
                               if (epoch_number - int(vouch_epoch)) == 45]
            if added_vouches or removed_vouches or expired_vouches:
                changed_received_vouches[address] = {
                   "added": added_vouches,
                   "removed": removed_vouches,
                   "expired": expired_vouches
                }
                print(f"DEBUG: Received vouches changed for {address}:")
                print(f"DEBUG: Added: {added_vouches}")
                print(f"DEBUG: Removed: {removed_vouches}")
                print(f"DEBUG: Expired: {expired_vouches}")

    # Detect changes in given vouches
    changed_given_vouches = {}
    for address in current_given_vouches:
        if address in previous_given_vouches:
            previous_vouches = previous_given_vouches[address]
            current_vouches = current_given_vouches[address]
            added_vouches = [vouch for vouch in current_vouches if vouch not in previous_vouches]
            removed_vouches = [vouch for vouch in previous_vouches if vouch not in current_vouches]
            expired_vouches = [vouch for vouch, vouch_epoch in previous_vouches.items()
                               if (epoch_number - int(vouch_epoch)) == 45]
            if added_vouches or removed_vouches or expired_vouches:
                changed_given_vouches[address] = {
                    "added": added_vouches,
                    "removed": removed_vouches,
                    "expired": expired_vouches
                }
                print(f"DEBUG: Given vouches changed for {address}:")
                print(f"DEBUG: Added: {added_vouches}")
                print(f"DEBUG: Removed: {removed_vouches}")
                print(f"DEBUG: Expired: {expired_vouches}")
                 

    with open(file_path, "w") as file:
        print_additional_info(file, epoch_number, set_size, pof_info, previous_pof_info)

        # Print bid info for qualified bidders
        file.write("\n\nQualified Bidders:\n")
        file.write("-" * (addr_width + handle_width + bid_width + total_width + unlocked_width + locked_width + 8) + "\n")
        file.write(header_format("Validator", "Handle", "Bid", "Total Balance", "Unlocked Balance", "Locked Balance", addr_width=addr_width, handle_width=handle_width, bid_width=bid_width, total_width=total_width, unlocked_width=unlocked_width, locked_width=locked_width))
        file.write("-" * (addr_width + handle_width + bid_width + total_width + unlocked_width + locked_width + 8) + "\n")

        for addr in current_bidders:
            formatted_address = f"({addr[2:6]}...{addr[-4:]})"
            discord_handle = get_discord_handle(addr)
            current_bid = current_bids.get(addr, 0)
            previous_bid = previous_bids.get(addr, None)

            # Format the bid with changes
            formatted_bid = format_bid_with_changes(current_bid, previous_bid)

            current_balance = current_balances.get(addr, {"total_balance": 0, "unlocked_balance": 0, "locked_balance": 0})
            previous_balance = previous_balances.get(addr, {"total_balance": 0, "unlocked_balance": 0, "locked_balance": 0})

            # Format the balance information with changes
            total_part, unlocked_part, locked_part = format_balances_with_changes(current_balance, previous_balance)

            # Output the current bid, balance, and changes
            file.write(row_format(formatted_address, discord_handle, formatted_bid, total_part, unlocked_part, locked_part, addr_width=addr_width, handle_width=handle_width, bid_width=bid_width, total_width=total_width, unlocked_width=unlocked_width, locked_width=locked_width))

        # Print auction winners
        file.write("\nAuction Winners:\n")
        file.write("-" * (addr_width + handle_width + bid_width + total_width + unlocked_width + locked_width + 8) + "\n")
        file.write(header_format("Validator", "Handle", "Bid", "Total Balance", "Unlocked Balance", "Locked Balance", addr_width=addr_width, handle_width=handle_width, bid_width=bid_width, total_width=total_width, unlocked_width=unlocked_width, locked_width=locked_width))
        file.write("-" * (addr_width + handle_width + bid_width + total_width + unlocked_width + locked_width + 8) + "\n")

        for addr in current_winners:
            formatted_address = f"({addr[2:6]}...{addr[-4:]})"
            discord_handle = get_discord_handle(addr)
            current_bid = current_bids.get(addr, 0)
            previous_bid = previous_bids.get(addr, None)

            # Format the bid with changes
            formatted_bid = format_bid_with_changes(current_bid, previous_bid)

            current_balance = current_balances.get(addr, {"total_balance": 0, "unlocked_balance": 0, "locked_balance": 0})
            previous_balance = previous_balances.get(addr, {"total_balance": 0, "unlocked_balance": 0, "locked_balance": 0})

            # Format the balance information with changes
            total_part, unlocked_part, locked_part = format_balances_with_changes(current_balance, previous_balance)

            # Output the current bid, balance, and changes
            file.write(row_format(formatted_address, discord_handle, formatted_bid, total_part, unlocked_part, locked_part, addr_width=addr_width, handle_width=handle_width, bid_width=bid_width, total_width=total_width, unlocked_width=unlocked_width, locked_width=locked_width))

        file.write("\n")
        
        print_seats_info(file, dropped_bidders, added_bidders, dropped_winners, added_winners, changed_bids, changed_received_vouches, changed_given_vouches, current_bids, previous_bids)

        print_jailed_validators(file, current_jail_info, previous_jail_info)
        
def print_seats_info(file, dropped_bidders, added_bidders, dropped_winners, added_winners, changed_bids, changed_received_vouches, changed_given_vouches, current_bids, previous_bids):
    try:
        # Emojis for indicators
        drop_icon = "❌"
        add_icon = "✅"
        change_icon = "⟲"
        vouch_icon = "🤝"
        revoke_icon = "🚫"
        lost_icon = "🔻"
        expired_icon = "⌛"

        # Formatting function for addresses
        def format_address(addr):
            return f"({addr[2:6]}...{addr[-4:]})"

        # Helper to format Discord handle and optionally the bid
        def format_discord_handle(addr, bid=None):
            handle = f"{get_discord_handle(addr)} {format_address(addr)}"
            if bid is not None and isinstance(bid, (int, float)):  # Check if bid is a valid number
                return f"{handle} (Bid: {bid})"
            return handle

        # Helper function to align table columns with a fixed width
        def align_text(left, middle, right, width_left=30, width_middle=15, width_right=30):
            left_aligned = f"{left:<{width_left}}"
            middle_aligned = f"{middle:<{width_middle}}"
            right_aligned = f"{right:<{width_right}}"
            return f"{left_aligned}{middle_aligned}{right_aligned}"
            
        if dropped_winners:
            file.write("\n**❌ Dropped from Auction Winners**\n")
            for addr in dropped_winners:
                file.write(f"  {format_discord_handle(addr, current_bids.get(addr))}\n")
        
        if added_winners:
            file.write("\n**✅ New Auction Winners**\n")
            for addr in added_winners:
                file.write(f"  {format_discord_handle(addr, current_bids.get(addr))}\n")

        if dropped_bidders:
            file.write("\n**❌ Dropped from Qualified Bidders**\n")
            for addr in dropped_bidders:
                file.write(f"  {format_discord_handle(addr, current_bids.get(addr))}\n")
        
        if added_bidders:
            file.write("\n**✅ Added to Qualified Bidders**\n")
            for addr in added_bidders:
                file.write(f"  {format_discord_handle(addr, current_bids.get(addr))}\n")       
        

        if changed_bids:
            file.write("\n**⟲ Bids Changed**\n")
            for addr, new_bid in changed_bids.items():
                old_bid = previous_bids.get(addr, "N/A")
                file.write(f"  {format_discord_handle(addr)} changed bid from {old_bid} to {new_bid}\n")

        if changed_received_vouches or changed_given_vouches:
            file.write("\n\n****🤝 Vouches Changed**\n")
            merged_vouches = {}  # Merging both given and received vouches

            # Merge received vouches
            for addr, vouch_info in changed_received_vouches.items():
                if addr not in merged_vouches:
                    merged_vouches[addr] = {'received': [], 'given': []}
                merged_vouches[addr]['received'] = vouch_info

            # Merge given vouches
            for addr, vouch_info in changed_given_vouches.items():
                if addr not in merged_vouches:
                    merged_vouches[addr] = {'received': [], 'given': []}
                merged_vouches[addr]['given'] = vouch_info

            # Initialize lists for different categories
            vouched_for_list = []
            revoked_list = []
            lost_list = []
            expired_list = []

            for addr, vouch_info in merged_vouches.items():
                discord_handle = format_discord_handle(addr)
                received = vouch_info.get('received', {})
                given = vouch_info.get('given', {})

                # Handle received vouches
                if received:
                    added_vouches = [f"{format_discord_handle(vouch)}" for vouch in received.get("added", [])]
                    removed_vouches = [f"{format_discord_handle(vouch)}" for vouch in received.get("removed", [])]
                    expired_vouches = [f"{format_discord_handle(vouch)}" for vouch in received.get("expired", [])]
                    
                    if added_vouches:
                        for vouch in added_vouches:
                            vouched_for_list.append(align_text(discord_handle, f"Received from {vouch_icon} ", vouch))
                    if removed_vouches:
                        for vouch in removed_vouches:
                            lost_list.append(align_text(discord_handle, f"Lost          {lost_icon} ", vouch))
                    if expired_vouches:
                        for vouch in expired_vouches:
                            expired_list.append(align_text(discord_handle, f"Vouch from    {expired_icon} ", vouch))

                # Handle given vouches
                if given:
                    added_vouches = [f"{format_discord_handle(vouch)}" for vouch in given.get("added", [])]
                    removed_vouches = [f"{format_discord_handle(vouch)}" for vouch in given.get("removed", [])]
                    expired_vouches = [f"{format_discord_handle(vouch)}" for vouch in given.get("expired", [])]
                    
                    if added_vouches:
                        for vouch in added_vouches:
                            vouched_for_list.append(align_text(discord_handle, f"Vouched for   {vouch_icon} ", vouch))
                    if removed_vouches:
                        for vouch in removed_vouches:
                            revoked_list.append(align_text(discord_handle, f"Revoked from  {revoke_icon} ", vouch))
                    if expired_vouches:
                        for vouch in expired_vouches:
                            expired_list.append(align_text(discord_handle, f"Vouch for     {expired_icon} ", vouch))

            # Write the grouped and ordered lists to the file
            if vouched_for_list:
                file.write("\n**✅ Vouched For**\n")
                for entry in vouched_for_list:
                    file.write(entry + "\n")

            if revoked_list:
                file.write("\n**🚫 Revoked**\n")
                for entry in revoked_list:
                    file.write(entry + "\n")

            if lost_list:
                file.write("\n**🔻 Lost**\n")
                for entry in lost_list:
                    file.write(entry + "\n")

            if expired_list:
                file.write("\n**⌛ Expired**\n")
                for entry in expired_list:
                    file.write(entry + "\n")

    except Exception as e:
        print(f"Error writing changes to file: {e}")
    
def print_additional_info(file, epoch_number, set_size, pof_info, previous_pof_info=None):
    try:
        # General epoch info
        file.write(f"Poorman's Newspaper - Epoch {epoch_number}\n")
        file.write("-" * 40 + "\n")
        file.write(f"Set Size: {set_size}\n")
        file.write("-" * 40 + "\n")

        # Helper function to format value changes
        def format_with_change(current, previous):
            if previous is not None:
                change = current - previous
                if change > 0:
                    return f"{current} (+{change})"
                elif change < 0:
                    return f"{current} ({change})"
                elif change == 0:
                    return f"{current}"
            return str(current)

        # Print Proof of Fee Information
        if pof_info:
            file.write("\nProof of Fee Information:\n")
            file.write("-" * 40 + "\n")

            # Extract previous values if they exist
            previous_clearing_bid = previous_pof_info.get('clearing_bid') if previous_pof_info else None
            previous_entry_fee = int(previous_pof_info.get('entry_fee'))/1000000 if previous_pof_info else None
            previous_median_win_bid = previous_pof_info.get('median_win_bid') if previous_pof_info else None
            previous_net_reward = int(previous_pof_info.get('net_reward'))/1000000 if previous_pof_info else None
            previous_nominal_reward = int(previous_pof_info.get('nominal_reward'))/1000000 if previous_pof_info else None
            
            entry_fee = int(pof_info.get('entry_fee'))/1000000
            net_reward = int(pof_info.get('net_reward'))/1000000
            nominal_reward = int(pof_info.get('nominal_reward'))/1000000
            

            # Format and print with changes
            file.write(f"Clearing Bid: {format_with_change(pof_info.get('clearing_bid'), previous_clearing_bid)}\n")
            file.write(f"Entry Fee: {format_with_change(entry_fee, previous_entry_fee)}\n")
            file.write(f"Median Win Bid: {format_with_change(pof_info.get('median_win_bid'), previous_median_win_bid)}\n")
            file.write(f"Net Reward: {format_with_change(net_reward, previous_net_reward)}\n")
            file.write(f"Nominal Reward: {format_with_change(nominal_reward, previous_nominal_reward)}\n")

            # Median history
            median_history = pof_info.get('median_history', [])
            above_950 = sum(1 for val in median_history if float(val) > 950)
            below_500 = sum(1 for val in median_history if float(val) < 500)

            file.write("\nMedian History:\n")
            file.write(f"Values: {', '.join(map(str, median_history))}\n")
            file.write(f"Epochs above 950: {above_950}\n")
            file.write(f"Epochs below 500: {below_500}\n")

        file.write("-" * 40 + "\n")
        
    except Exception as e:
        print(f"Error writing additional info to file: {e}")
        
def print_jailed_validators(file, current_jail_info, previous_jail_info=None):
    try:
        file.write("\nJailed Validators Report:\n")
        file.write("-" * 40 + "\n")
        
        # Iterate through all validators in the current jail info
        for validator_address, jail_info in current_jail_info.items():
            previous_jail_info_for_validator = previous_jail_info.get(validator_address) if previous_jail_info else None

            # Check if the validator is currently jailed
            if jail_info['is_jailed']:
                # Determine if the validator was jailed in the current epoch
                has_been_jailed_recently = previous_jail_info_for_validator is None or not previous_jail_info_for_validator['is_jailed']

                # Format the jailed status
                jailed_status = ""
                if has_been_jailed_recently:
                    jailed_status += " (Newly Jailed in this Epoch)"

                # Print the validator's address and jail status
                formatted_address = f"({validator_address[2:6]}...{validator_address[-4:]})"
                discord_handle = get_discord_handle(validator_address)
                file.write(f"{discord_handle} {formatted_address} {jailed_status}\n")

                # Format and print the vouchees jailed count, lifetime jailed, and consecutive failures
                vouchees_jailed_count = jail_info['vouchees_jailed_count']
                lifetime_jailed = jail_info['lifetime_jailed']
                consecutive_failure_to_rejoin = jail_info['consecutive_failure_to_rejoin']

                #file.write(f"  Vouchees Jailed Count: {vouchees_jailed_count}\n")
                #file.write(f"  Lifetime Jailed: {lifetime_jailed}\n")
                #file.write(f"  Consecutive Failures to Rejoin: {consecutive_failure_to_rejoin}\n")
                #file.write("-" * 40 + "\n")

    except Exception as e:
        print(f"Error writing jailed validators to file: {e}")

# Function to get the Discord handle from an address
def get_discord_handle(address):
    return address_to_discord.get(address, "Unknown")

def get_qualified_bidders():
    command = "libra query view --function-id 0x1::epoch_boundary::get_qualified_bidders"
    result = subprocess.check_output(command, shell=True)
    data = json.loads(result.decode())
    if "body" in data and len(data["body"]) > 0:
        return data["body"][0]  # The list of qualified bidders is in the first element of "body"
    return []
    
def get_auction_winners():
    command = "libra query view --function-id 0x1::epoch_boundary::get_auction_winners"
    result = subprocess.check_output(command, shell=True)
    data = json.loads(result.decode())
    if "body" in data and len(data["body"]) > 0:
        return data["body"][0]  # The list of qualified bidders is in the first element of "body"
    return []
    
def get_eligible_validators():
    print("Querying eligible validators...")
    command = "libra query view --function-id 0x1::validator_universe::get_eligible_validators"
    result = subprocess.check_output(command, shell=True)
    data = json.loads(result.decode())
    if "body" in data and len(data["body"]) > 0:
        print(f"Found {len(data['body'][0])} eligible validators.")
        return data["body"][0]  # The list of eligible validators is in the first element of "body"
    return []
    
def get_number_of_seats_offered():
    try:
        command = "libra query view --function-id 0x1::epoch_boundary::get_seats_offered"
        result = subprocess.check_output(command, shell=True)
        json_data = json.loads(result.decode())

        if "body" in json_data and isinstance(json_data["body"], list) and len(json_data["body"]) > 0:
            return int(json_data["body"][0])
        else:
            raise ValueError("Unexpected format in JSON output.")

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None
    except ValueError as ve:
        print(ve)
        return None


def get_validator_addresses():
    qualified_bidders = get_qualified_bidders()
    auction_winners = get_auction_winners()
    seats_offered = get_number_of_seats_offered()
    elligible_validators = get_eligible_validators()
    print("Incoming Qualified Bidders:", qualified_bidders)
    print("Incoming Auction Winners:", auction_winners)
    return qualified_bidders, auction_winners, seats_offered, elligible_validators

def query_validator_bid(validator_address, current_epoch):
    command = f"libra query resource --resource-path-string 0x1::proof_of_fee::ProofOfFeeAuction {validator_address}"
    result = subprocess.check_output(command, shell=True)
    bid_data = json.loads(result.decode())
    if (int(bid_data["epoch_expiration"]) < current_epoch):
       return -1;
    return int(bid_data["bid"])
    

def get_current_epoch():
    try:
        # Execute the command to get the current epoch data
        command = "libra query resource --resource-path-string 0x1::epoch_boundary::BoundaryBit 0x1"
        result = subprocess.check_output(command, shell=True)
        data = json.loads(result.decode())

        # Extract the closing_epoch value from the JSON data
        closing_epoch = data.get("closing_epoch")
        if closing_epoch is not None:
            return int(closing_epoch)
        else:
            raise ValueError("The 'closing_epoch' key was not found in the JSON response.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        raise
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        raise
    except ValueError as ve:
        print(f"Value error: {ve}")
        raise
        
def get_vouches(validator_address):
    received_command = f"libra query view --function-id 0x1::vouch::get_received_vouches --args {validator_address}"
    given_command = f"libra query view --function-id 0x1::vouch::get_given_vouches --args {validator_address}"
    
    received_result = subprocess.check_output(received_command, shell=True)
    given_result = subprocess.check_output(given_command, shell=True)
    
    received_data = json.loads(received_result.decode())
    given_data = json.loads(given_result.decode())
    
    def parse_vouches(data):
        addresses = data["body"][0] if len(data["body"]) > 0 else []
        epochs = data["body"][1] if len(data["body"]) > 1 else []
        vouches_dict = dict(zip(addresses, epochs))
        return vouches_dict

    return {
        "received_vouches": parse_vouches(received_data),
        "given_vouches": parse_vouches(given_data),
    }

def fetch_vouches_for_validator(validator_address):
    try:
        vouches = get_vouches(validator_address)
        return validator_address, vouches
    except Exception as e:
        print(f"Error retrieving vouches for {validator_address}: {e}")
        return validator_address, None
        

def fetch_all_vouches(addresses):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_vouches_for_validator, addr): addr for addr in addresses}
        results = {}
        for future in concurrent.futures.as_completed(futures):
            address, vouches = future.result()
            if vouches is not None:
                results[address] = vouches
        return results
        
def get_balances(validator_address):
    balance_command = f"libra query balance {validator_address}"    
    balance_result = subprocess.check_output(balance_command, shell=True)    
    balance_data = json.loads(balance_result.decode())

    def parse_balances(data):
        unlocked_balance = data.get("unlocked", 0)
        total_balance = data.get("total", 0)
        locked_balance = total_balance - unlocked_balance  # Calculate locked balance
        return {
            "unlocked_balance": unlocked_balance,
            "locked_balance": locked_balance,
            "total_balance": total_balance,            
        }

    return parse_balances(balance_data)
        
def fetch_balances_for_validator(validator_address):
    try:
        balances = get_balances(validator_address)
        return validator_address, balances
    except Exception as e:
        print(f"Error retrieving balances for {validator_address}: {e}")
        return validator_address, None
        
def fetch_all_balances(addresses):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_balances_for_validator, addr): addr for addr in addresses}
        results = {}
        for future in concurrent.futures.as_completed(futures):
            address, balances = future.result()
            if balances is not None:
                results[address] = balances
        return results

def print_vouches_info(title, addresses):
    print(title)
    print("-" * 40)
    vouches_dict = fetch_all_vouches(addresses)
    for address in addresses:
        vouches = vouches_dict.get(address, None)
        if vouches:
            formatted_address = f"({address[2:6]}...{address[-4:]})"
            discord_handle = get_discord_handle(address)
            received_vouches = [f"{addr[:6]}...{addr[-4:]} ({epoch})" for addr, epoch in vouches["received_vouches"].items()]
            given_vouches = [f"{addr[:6]}...{addr[-4:]} ({epoch})" for addr, epoch in vouches["given_vouches"].items()]
            print(f"Validator: {formatted_address}, Handle: {discord_handle}")
            print(f"  Received Vouches: {', '.join(received_vouches) if received_vouches else 'None'}")
            print(f"  Given Vouches: {', '.join(given_vouches) if given_vouches else 'None'}")
            print("\n")
        else:
            print(f"Validator: {address} not found or has no vouches.")

def print_bid_info(title, addresses, bids):
    print(title)
    print("-" * 40)
    # Sort the addresses and bids based on bids in descending order
    sorted_info = sorted(zip(addresses, bids), key=lambda x: x[1], reverse=True)
    for address, bid in sorted_info:
        formatted_address = f"({address[2:6]}...{address[-4:]})"
        discord_handle = get_discord_handle(address)
        print(f"Validator: {formatted_address}, Bid: {bid}, Handle: {discord_handle}")
    print("\n")
    
def print_set_to_file(filename, qualified_bidders, auction_winners):
    try:
        with open(filename, "w") as file:
            # Print bid info for qualified bidders and auction winners to the file
            file.write("Qualified Bidders:\n")
            file.write("-" * 40 + "\n")
            for addr in qualified_bidders:
                formatted_address = f"({addr[2:6]}...{addr[-4:]})"
                discord_handle = get_discord_handle(addr)
                file.write(f"Validator: {formatted_address}, Handle: {discord_handle}\n")
            file.write("\nAuction Winners:\n")
            file.write("-" * 40 + "\n")
            for addr in auction_winners:
                formatted_address = f"({addr[2:6]}...{addr[-4:]})"
                discord_handle = get_discord_handle(addr)
                file.write(f"Validator: {formatted_address}, Handle: {discord_handle}\n")
            file.write("\n")
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")
        
def get_proof_of_fee_info():
    try:
        # Command to query the proof of fee information
        command = "libra query resource --resource-path-string 0x1::proof_of_fee::ConsensusReward 0x1"
        result = subprocess.check_output(command, shell=True)
        
        # Decode the JSON output
        data = json.loads(result.decode())

        # Extract all relevant fields from the response
        proof_of_fee_info = {
            "clearing_bid": int(data.get("clearing_bid", None)),
            "entry_fee": int(data.get("entry_fee", None)),
            "median_history": data.get("median_history", []),
            "median_win_bid": int(data.get("median_win_bid", None)),
            "net_reward": int(data.get("net_reward", None)),
            "nominal_reward": int(data.get("nominal_reward", None)),
        }

        # Print or return the extracted fields
        print("Proof of Fee Information:")
        for key, value in proof_of_fee_info.items():
            print(f"{key}: {value}")
        
        return proof_of_fee_info

    except subprocess.CalledProcessError as e:
        print(f"PoF Info Command failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode PoF Info JSON.")
        return None  


def is_validator_jailed(validator_address):
    try:
        command = f"libra query view --function-id 0x1::jail::is_jailed --args {validator_address}"
        result = subprocess.check_output(command, shell=True)
        data = json.loads(result.decode())
        # Parse the value from the "body"
        is_jailed = data.get("body", [False])[0]
        return is_jailed
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None
        
def get_vouchees_jailed_count(validator_address):
    try:
        command = f"libra query view --function-id 0x1::jail::get_count_buddies_jailed --args {validator_address}"
        result = subprocess.check_output(command, shell=True)
        data = json.loads(result.decode())
        # Parse the jailed vouchees count from the "body"
        vouchees_jailed_count = int(data.get("body", ["0"])[0])
        return vouchees_jailed_count
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None
        
def get_jail_reputation(validator_address):
    try:
        command = f"libra query view --function-id 0x1::jail::get_jail_reputation --args {validator_address}"
        result = subprocess.check_output(command, shell=True)
        data = json.loads(result.decode())
        # Parse the lifetime jailed and consecutive failures from the "body"
        jail_reputation = {
            "lifetime_jailed": int(data.get("body", ["0", "0"])[0]),
            "consecutive_failure_to_rejoin": int(data.get("body", ["0", "0"])[1])
        }
        return jail_reputation
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None
        
def fetch_jail_info_for_validator(validator_address):
    is_jailed = is_validator_jailed(validator_address)
    vouchees_jailed_count = get_vouchees_jailed_count(validator_address)
    jail_reputation = get_jail_reputation(validator_address)

    # Return all jail-related info as a dictionary
    return {
        "is_jailed": is_jailed,
        "vouchees_jailed_count": vouchees_jailed_count,
        "lifetime_jailed": jail_reputation.get("lifetime_jailed", 0),
        "consecutive_failure_to_rejoin": jail_reputation.get("consecutive_failure_to_rejoin", 0)
    }


def fetch_all_jail_info(addresses):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all validator addresses for jail info fetching
        futures = {executor.submit(fetch_jail_info_for_validator, addr): addr for addr in addresses}
        results = {}

        # Gather results as they complete
        for future in concurrent.futures.as_completed(futures):
            address = futures[future]
            try:
                jail_info = future.result()
                if jail_info is not None:
                    results[address] = jail_info
            except Exception as e:
                print(f"Error fetching jail info for {address}: {e}")
        
        return results        

def main():
    current_epoch = None
    previous_epoch = None
    previous_filepath = None
    current_filepath = None
    newspaper_filepath = None
    previous_run_file_path = None
    qualified_bidders = []
    auction_winners = []
    seats_offered = None
    
    

    try:
        # Get the current epoch number
        os.makedirs(DATA_FOLDER, exist_ok=True)
        current_epoch = get_current_epoch()
        previous_epoch = current_epoch - 1
        
        print(f"Comparing the current epoch {current_epoch} and the previous epoch {previous_epoch}")

        # Define file paths
        previous_filepath = os.path.join(DATA_FOLDER, f"poormans_epoch_{previous_epoch}.json")
        current_filepath = os.path.join(DATA_FOLDER, f"poormans_epoch_{current_epoch}.json")
        newspaper_filepath = os.path.join(DATA_FOLDER, f"poormans_epoch_{current_epoch}.txt")
    except Exception as e:
        print(f"Error retrieving epoch number or defining file paths: {e}")
        return

    try:
        # Get the validator addresses
        qualified_bidders, auction_winners, seats_offered, elligible_validators = get_validator_addresses()
    except Exception as e:
        print(f"Error retrieving validator addresses: {e}")
        return

    previous_run = {}
    try:
        # Load previous run data
        previous_run = load_previous_run(previous_filepath)
    except Exception as e:
        print(f"Error loading previous run data: {e}")

    # Safely handle missing keys with .get() method
    previous_bidders = previous_run.get("qualified_bidders", [])
    previous_winners = previous_run.get("auction_winners", [])
    previous_bids = previous_run.get("bids", {})
    previous_vouches = previous_run.get("vouches", {})
    previous_balances = previous_run.get("balances", {})
    previous_jail_info = previous_run.get("jail_info", {})
    previous_pof_info = previous_run.get("pof_info", {})


    current_bids = {}
    current_vouches = {}
    current_balances = {}
    pof_info = {}
    
    try:
        pof_info = get_proof_of_fee_info()
    except Exception as e:
        print(f"Error retrieving PoF info: {e}")
        return

    try:
        # Fetch bids for current qualified bidders in parallel
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(query_validator_bid, address, current_epoch): address for address in elligible_validators}
            for future in futures:
                address = futures[future]
                try:
                    current_bids[address] = future.result()
                except Exception as e:
                    print(f"Error fetching bid for {address}: {e}")
    except Exception as e:
        print(f"Error with concurrent bid fetching: {e}")

    try:
        # Fetch vouches for current qualified bidders using the fetch_all_vouches function
        current_vouches = fetch_all_vouches(elligible_validators)
    except Exception as e:
        print(f"Error with concurrent vouch fetching: {e}")
        
    try:
        # Fetch balances for current qualified bidders using the fetch_all_balances function
        current_balances = fetch_all_balances(elligible_validators)
    except Exception as e:
        print(f"Error with concurrent balance fetching: {e}")
        
    try:
        # Fetch jail info for current qualified bidders using the fetch_all_jail_info function
        current_jail_info = fetch_all_jail_info(elligible_validators)
    except Exception as e:
        print(f"Error with concurrent balance fetching: {e}")

    try:
        # Display relevant seat information
        print(f"Seats Offered: {seats_offered}, Seats Taken: {len(auction_winners)}")
    except Exception as e:
        print(f"Error displaying seat information: {e}")

    try:
        # Print the bid info for qualified bidders and auction winners
        print_bid_info("Qualified Bidders", qualified_bidders, [current_bids.get(addr, 'N/A') for addr in qualified_bidders])
        auction_bids = [current_bids.get(addr, 'N/A') for addr in auction_winners]
        print_bid_info("Auction Winners", auction_winners, auction_bids)
    except Exception as e:
        print(f"Error printing bid information: {e}")

    #try:
        # Print vouches information
        #print_vouches_info("Vouches Information", qualified_bidders)
    #except Exception as e:
        #print(f"Error printing vouches information: {e}")
    #print(f"\n\nCUR VCH: {current_vouches}")
    #print(f"\n\nPREV VCH: {previous_vouches}")
    
    # Sort the qualified bidders and auction winners by their bids in descending order
    sorted_qualified_bidders = sorted(qualified_bidders, key=lambda addr: current_bids.get(addr, 0), reverse=True)
    sorted_auction_winners = sorted(auction_winners, key=lambda addr: current_bids.get(addr, 0), reverse=True)
    try:
        # Compare current run with the previous run data and save results
        compare_runs(
            current_bidders=sorted_qualified_bidders,
            current_winners=sorted_auction_winners,
            current_bids=current_bids,
            current_vouches=current_vouches,
            current_balances=current_balances,
            current_jail_info=current_jail_info,
            previous_bidders=previous_bidders,
            previous_winners=previous_winners,
            previous_bids=previous_bids,
            previous_vouches=previous_vouches,
            previous_balances=previous_balances,
            previous_jail_info=previous_jail_info,
            epoch_number=current_epoch,
            set_size=len(auction_winners),
            pof_info=pof_info,
            previous_pof_info=previous_pof_info,
            file_path=newspaper_filepath
        )
    except Exception as e:
        print(f"Error comparing runs or printing to file: {e}")

    try:
        # Save the current run data
        save_current_run(
            qualified_bidders=qualified_bidders,
            auction_winners=auction_winners,
            bids=current_bids,
            vouches=current_vouches,
            balances=current_balances,
            jail_info=current_jail_info,
            pof_info=pof_info,
            filepath=current_filepath
        )
         # Trigger file creation AFTER the main file is complete
        with open("/home/ubuntu/libra-framework/epoch_data/trigger_file.txt", "w") as trigger_file:
            # Write the current epoch into the trigger file
            trigger_file.write(f"{current_epoch}")

        print("Trigger file created. Waiting for bot to send the file.")


    except Exception as e:
        print(f"Error saving current run data: {e}")
        
    

if __name__ == "__main__":
    main()
