#!/bin/bash
# usage: studio/titled_copy.sh <video.mp4> "<Video Title>"  -> renders/titled/<Video Title>.mp4 (send THIS file to the owner so the download has the title as its name)
set -e
src="$1"; title="$2"; mkdir -p "$(dirname "$0")/../renders/titled"
safe=$(echo "$title" | sed 's/[\/:*?"<>|]/-/g')
dst="$(cd "$(dirname "$0")/.." && pwd)/renders/titled/$safe.${src##*.}"
cp "$src" "$dst"; echo "$dst"
