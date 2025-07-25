import asyncio
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest, ForwardMessagesRequest
from telethon.errors import FloodWaitError, MessageIdInvalidError
import os

# ================= CONFIG =================

api_id = 28403662
api_hash = '079509d4ac7f209a1a58facd00d6ff5a'

source_channel = 'https://t.me/LAKSHYA_NEET_2025_LECTURE_FREE'
group_invite = 'sDEu9mrBb4JlMTNl'

session_name = 'anon'
progress_file = 'last_id_11th.txt'

# ============== Progress Save/Load ==============

def save_last_id(last_id):
    with open(progress_file, 'w') as f:
        f.write(str(last_id))

def load_last_id():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return int(f.read().strip())
    return 0

# ============== Main Logic ==============

async def main():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("✅ Connected to Telegram")

        try:  
            target = await client(ImportChatInviteRequest(group_invite))  
            print("✅ Joined group via invite link")  
        except:  
            target = await client.get_entity(f'https://t.me/+{group_invite}')  
            print("✅ Already a member of the group")  

        source = await client.get_entity(source_channel)  
        last_id = load_last_id()  
        print(f"▶️ Resuming from message ID: {last_id +1}")  

        count = 0  
        async for message in client.iter_messages(source, min_id=last_id, reverse=True):  
            if not message or not message.message:  
                continue  # skip non-text or service messages  

            try:  
                await client(ForwardMessagesRequest(  
                    from_peer=source,  
                    id=[message.id],  
                    to_peer=target  
                ))  
                print(f"✅ Forwarded: {message.id}")  
                save_last_id(message.id)  
                count += 1  
                await asyncio.sleep(1.5)  

            except FloodWaitError as e:  
                print(f"⏳ Flood wait: {e.seconds} seconds. Waiting...")  
                time.sleep(e.seconds + 5)  
                continue  

            except MessageIdInvalidError:  
                print(f"⚠️ Skipped invalid message ID: {message.id}")  
                continue  

            except Exception as e:  
                print(f"❌ Unknown error on message {message.id}: {e}")  
                break  

        if count == 0:  
            print("✅ Nothing to forward or already done.")  
        else:  
            print(f"🎉 Done. Forwarded {count} messages.")

# ============== RUN ==============

asyncio.run(main())
