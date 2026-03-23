# Testimonials

Monitors ad forum threads and collects feedback from users who found an editor through the server.

## How it works

1. Bot watches configured forum channels (free ad, paid ad)
2. After a configurable delay, bot sends a reminder asking if the user found an editor
3. User clicks "Found Editor" and goes through a multi-step flow: pick the editor, job type, star rating, write feedback
4. Completed testimonials post to the output channel as a gold embed
5. If user clicks "Still Looking", the reminder timer resets

## Thread lifecycle

- Threads are tracked from creation
- Reminder sent after the configured time (default varies by channel)
- Once a testimonial is submitted or the thread is closed, tracking stops
- Thread is locked and archived after completion

## Configuration

All settings managed via `/testimonial_config` (Tier 0):

- Watched channels: which forum channels to monitor
- Output channel: where completed testimonials get posted
- Job types: dropdown options for the testimonial form
- Timing: how long to wait before sending reminders
