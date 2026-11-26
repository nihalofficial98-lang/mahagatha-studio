# Project rules for Claude

**File name rule (owner):** whenever a video is sent to the owner, the file name must be the video title (for example "EP07 - Kacha Steals the Secret of the Dead.mp4" or "Reel 5 - How Was Shiva Born.mp4"), so the downloaded file has its title as the name. Copy the video with `studio/titled_copy.sh <video> "<Title>"` and send that copy with SendUserFile. Never send files named like `ep07_scored_1080p.mp4`.

**Calendar rule (owner):** the posting calendar is the Google-style Sheet at https://claude.ai/artifact/7LK5C8NFniARNdbLbjJZzN (Claude Docs project id 334919dc-b58d-4f0e-8f1f-259bde2d6bc7, sheet "Calendar", columns Date, Day, Type, Title, Status, Thumbnail, Notes). Whenever a video, reel, thumbnail or script is finished, recorded, rendered or posted, or the owner changes a date or title, update its row in the same turn (Status: Needs recording / Ready to post / Posted; Thumbnail: Needed / Prompt ready / Done). Read the sheet first, since the owner edits it too. Also keep deliverables/Posting_Calendar_27Nov-11Dec.md in step only if the owner asks.

**Posted column rule (owner):** column H "Posted? (you set this)" of the calendar belongs to the owner (Not posted / Posted). Each time I read the calendar, for every row where H is Posted, set Status (column E) to Posted and leave H alone. Never change H myself.
