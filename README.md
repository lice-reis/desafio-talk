# Instagram Communities — App Redesign Challenge

A frontend-only prototype of a new **Communities** feature for Instagram, built for a 10-minute class presentation (App Redesign Challenge, English course).

This repository holds everything needed to design and build the prototype: the feature guidelines below, seeded mock data in `data/`, and local photos in `assets/`. No backend. Everything runs offline.

**Demo community:** Trail Run BR, a private community of trail runners in Brazil.

---

## 1. The idea in one paragraph

Instagram connects you to everyone, but not to *your people*. Communities are private or public spaces inside Instagram with their own feed and their own stories, exclusive to members. They work like Facebook Groups (own feed, member list, rules, admin) but reuse the Instagram interface people already know. Nothing posted in a community can be shared outside of it.

## 2. Principles

1. **Reuse Instagram's UI.** Communities must look like Instagram, not like a new app. Same icons, same feed layout, same story rings, same bottom sheets, same typography. Light and dark mode.
2. **Nothing leaves the community.** There is no Share action anywhere inside a community: not on posts, not on stories. No "send to", no reposting, no copy link.
3. **Facebook Groups as behavioral reference** for the side menu (About, Rules, Members, Privacy) and for the public/private model. Instagram as visual reference for everything else.
4. **Mobile only.** The prototype is a phone screen (390×844) centered on a desktop page. Everything must fit inside the frame with no overflow.
5. **Fully mocked.** All content comes from `data/*.json` and `assets/`. State lives in memory (optionally `localStorage`). A **Reset demo** control restores the seeded state.

## 3. Navigation

The Instagram bottom tab bar gets a **sixth icon**: Communities (two-people silhouette).

Order, left to right: **Home · Reels · DMs · Search · Communities · Profile**

Tapping it opens the **Communities hub**.

## 4. Screens

### 4.1 Communities hub

- Header: "Communities".
- **Your communities:** a list of the communities the user belongs to. Each row shows a round profile picture, the name, member count, and a small **Public** or **Private** label. No cover images (Instagram doesn't have them).
- **Discover:** a grid of post previews, styled like Instagram's Explore grid. Each tile is a photo with the source community's name and round avatar overlaid on the bottom. Tiles never open.
- Only **Trail Run BR** is navigable. Every other community is a static row or tile. Do not build screens for them.

Data: `data/communities.json`.

### 4.2 Community feed (Trail Run BR)

Layout is the Instagram home feed, adapted:

- **Header:** back arrow · round community avatar + name · **➕** (create post) · **🔍** (search) · **☰** (menu). Header is sticky.
- **Stories row** at the top, with a small segmented control above it: **Current | Fixed**. See section 5.
- **Feed:** posts in Instagram's post layout. Photo, author avatar + username, caption, likes count, comments, relative time.
- **Post actions:** ❤️ Like · 💬 Comment · 🔖 Save. **No share icon.** Double-tap to like works.
- **Comments** open as a bottom sheet. The user can add a comment.
- A small lock icon with "Only members can see this" sits under the header, once, as a reminder that the feed is exclusive.

Data: `data/posts.json` (10 posts, each with its own personality: group-run invite, shoe question, sunrise photo, race recap, viewpoint break, trail safety alert, physio tip, newcomer intro, lake stop, admin reminder). Posts have no standardized metrics field; they are ordinary Instagram posts with free captions.

### 4.3 Create post (➕)

Bottom sheet or full screen in Instagram's "New post" style:

1. Pick a photo from a small local gallery (reuse images in `assets/posts/` and `assets/stories/`).
2. Write a caption.
3. Tap **Share to Trail Run BR**.

The new post appears at the top of the feed with a short entrance animation and a toast "Shared to Trail Run BR". Only the file picker is simulated; there is no real upload.

### 4.4 Search (🔍)

Full-screen search over the community's posts only. Filters by caption text, username or hashtag, live as the user types. Results use the same post layout or a compact grid. Empty state: "No posts found in Trail Run BR".

### 4.5 Side menu (☰)

Slides in from the right. Modeled on Facebook Groups' "About" panel:

- **About:** description, created date, location.
- **Privacy:** Private, with a one-line explanation.
- **Rules:** numbered list with title + description.
- **Members:** member count, search field, list with the **Admin** at the top (crown or "Admin" badge), then everyone else. Each row: avatar, name, @username, joined date.
- **Leave community** (visible to Member only).
- **Settings** (visible to Admin only). It exists as a menu item and does **not** open anything. It is there to show that the admin controls the community.

Data: `data/community.json` and `data/members.json`.

### 4.6 Story viewer

Instagram's full-screen story viewer:

- Progress bars at the top, one per story of that author.
- Tap right / left to go next / previous. Hold to pause. Swipe down to close.
- Author avatar, username and relative time at the top. Optional text overlay on the image.
- Reply field at the bottom ("Reply to @username…"). **No "send to" and no share.**
- **⋯ menu:** for the Admin, contains **Pin to community** (on a current story) or **Unpin** (on a fixed story). For Member and Visitor, the ⋯ menu has no pin option at all; do not show it disabled, do not show it.

### 4.7 Visitor screen

When the user is not a member of a private community:

- Community avatar, name, "Private · 1,284 members", About text and Rules.
- Feed and stories are not rendered. A lock illustration and the text "This community is private. Join to see posts and stories."
- Primary button: **Request to join**. Tapping it changes the button to "Requested" (disabled). Nothing else happens.

## 5. Stories: Current and Fixed

The stories row has two views, switched by the segmented control **Current | Fixed**.

### Current

- Stories posted by members inside the community. Behave exactly like Instagram stories today: 24-hour lifetime, gradient ring, one ring per author, several stories per author.
- First ring is **Your story** with a ➕ to add one (pick a local photo, optional text, post). It appears immediately.
- Seeded with **20 stories across 6 members** (`data/stories.json → current`).

### Fixed

- Stories the Admin pinned. Behave like Instagram highlights: **no limit and no expiration** while pinned.
- Same ring layout, one ring per author, with the author's avatar and username under it. A small pin icon on the ring.
- Seeded with **10 stories across 5 members** (`data/stories.json → fixed`).

### Pinning rules

| Rule | |
|---|---|
| Who can pin | **Only the Admin.** |
| What can be pinned | **Any** member's current story, including the admin's own. |
| Where | The ⋯ menu inside the story viewer: **Pin to community**. |
| Effect | The story moves from Current to Fixed immediately, keeps the original author's credit, and stops expiring. |
| Unpin | Only the Admin, via ⋯ → **Unpin** on a fixed story. It returns to Current if still within 24h, otherwise disappears. |
| Limit | None. |
| Notification | None. (Instagram doesn't notify for highlights.) |
| Members and visitors | Never see the pin option. |

## 6. Roles and demo mode

The current user is always **@alice.reis**. A floating **Demo mode** control **outside the phone frame** (clearly a presenter control, never part of the Instagram UI) switches her role with no page reload:

| | Admin | Member | Visitor |
|---|---|---|---|
| See feed and stories | ✅ | ✅ | ❌ (visitor screen) |
| Post, comment, like, save | ✅ | ✅ | ❌ |
| Post a story | ✅ | ✅ | ❌ |
| Pin / Unpin stories | ✅ | ❌ | ❌ |
| Settings in menu | ✅ | ❌ | ❌ |
| Leave community in menu | ❌ | ✅ | ❌ |
| Members list | @alice.reis at top with Admin badge | @mari.trail at top with Admin badge | not visible |

When Alice is not the admin, **@mari.trail** is shown as the admin (see `data/members.json`).

Next to the role switch: a **Reset demo** button that restores all seeded data (posts, likes, comments, stories, pins, join request).

## 7. Live demo script (what must work without failing)

1. Tap the Communities tab, see Your communities and the Discover grid.
2. Open **Trail Run BR**, scroll the exclusive feed.
3. Tap ➕, pick a photo, write a caption, share. The post appears on top.
4. Tap **Your story**, pick a photo, post. The ring appears in Current.
5. Open a member's story, tap ⋯. As **Member**, there is no pin option.
6. Switch to **Admin**, open the same story, tap ⋯ → **Pin to community**. Switch the row to **Fixed**: the story is there, credited to its author.
7. Open ☰: About, Rules, Members with the Admin badge, and the Settings item.
8. Switch to **Visitor**: locked screen with **Request to join**.

## 8. Out of scope

Login, creating a community, moderation and reporting, DMs, recommendation algorithm, real file upload, the Settings screen, screens for any community other than Trail Run BR, notifications, sharing of any kind, editing rules or privacy.

## 9. Repository layout

```
data/
  communities.json   hub list, discover list and discover grid tiles
  community.json     Trail Run BR: about, privacy, rules, menu items
  members.json       members, current user, default admin
  posts.json         10 seeded feed posts with comments
  stories.json       20 current + 10 fixed seeded stories
assets/
  posts/        10 photos (4:5 / square)      feed posts
  stories/      30 photos (9:16)              stories, also usable as picker options
  avatars/      member profile pictures
  communities/  community profile pictures
  discover/     24 square photos for the Discover grid
  credits.json  photographer credits for every photo
scripts/
  fetch_photos.py    how the photos were obtained (already run, no need to run again)
```

All image paths in the JSON files are relative to the repository root.

## 10. Photo credits

All photos are from [Unsplash](https://unsplash.com) under the [Unsplash License](https://unsplash.com/license). Photographer and source link for every file are listed in `assets/credits.json`.
