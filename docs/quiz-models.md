# Quiz Models Documentation

**Status:** ✅ Implemented (Migration Pending)
**Last Updated:** 2025-11-20
**Django App:** `quiz`

---

## Overview

The quiz app implements a single-player quiz game system with time tracking, statistics, and
achievements. The data model consists of 7 core models that handle categories, questions, game
sessions, attempts, user statistics, and trophies.

---

## Data Models

### 1. Category

**Purpose:** Organize questions into different programming categories.

**Table:** `quiz_category`

**Fields:**
- `name` (CharField, unique) - Category identifier with choices:
  - `HTML` - HTML questions
  - `PYTHON` - Python questions
  - `DJANGO` - Django questions
  - `JS` - JavaScript questions
  - `CSS` - CSS questions
  - `RANDOM` - Random category
  - `CUSTOM` - Custom category
- `description` (TextField, blank) - Category description
- `icon_class` (CharField, blank) - FontAwesome icon class (e.g., `fa-brands fa-html5`, `fa-brands fa-python`)
- `prism_language` (CharField, blank) - Prism.js language identifier for syntax highlighting (e.g., `html`, `python`, `javascript`)
- `order` (PositiveIntegerField) - Display order (default: 0)

**Meta:**
- Ordering: `['order', 'name']`
- Verbose Name: "category" / "categories"

**Admin Features:**
- List display: name, translated name, order
- Filters: (none)
- Search: name, description

---

### 2. Question

**Purpose:** Store quiz questions with code snippets, answers, and explanations.

**Table:** `quiz_question`

**Fields:**
- `category` (ForeignKey → Category) - Question category
- `difficulty` (CharField) - Difficulty level with choices:
  - `BEGINNER` - Beginner level
  - `INTERMEDIATE` - Intermediate level
  - `ADVANCED` - Advanced level
  - `EXPERT` - Expert level
- `question_text` (JSONField) - Bilingual question text: `{"en": "...", "zh": "..."}`
- `code_snippet` (TextField, blank) - Optional code snippet
- `answer` (CharField, max 100) - Correct answer (case-insensitive)
- `hint_text` (JSONField, blank) - Bilingual hint: `{"en": "...", "zh": "..."}`
- `explanation` (JSONField, blank) - Bilingual explanation: `{"en": "...", "zh": "..."}`
- `is_active` (BooleanField) - Whether question is active (default: True)
- `created_at` (DateTimeField, auto) - Creation timestamp
- `updated_at` (DateTimeField, auto) - Last update timestamp

**Methods:**
- `get_question_text(language='en')` - Get question in specified language
- `get_hint_text(language='en')` - Get hint in specified language
- `get_explanation(language='en')` - Get explanation in specified language
- `clean_answer()` - Returns normalized answer (lowercase, stripped)

**Meta:**
- Ordering: `['-created_at']`
- Indexes:
  - `(category, difficulty, is_active)`
  - `(-created_at)`

**Admin Features:**
- List display: ID, shortened question, category, difficulty, active status, created date
- Filters: category, difficulty, is_active, created_at
- Search: question_text, answer, code_snippet
- Fieldsets: Basic Info, Question Content, Help & Explanation, Metadata

---

### 3. GameSession

**Purpose:** Track a user's attempt at answering a single question with time-based completion.

**Table:** `quiz_game_session`

**Fields:**
- `user` (ForeignKey → User) - Player attempting the question
- `question` (ForeignKey → Question) - Question being attempted
- `started_at` (DateTimeField, auto) - When session started
- `end_at` (DateTimeField) - Timer deadline (when session expires)
- `completed_at` (DateTimeField, nullable) - When user submitted final answer
- `score` (IntegerField, default: 0) - Score earned

**Properties:**
- `status` - **@property (computed)** - Calculates current status from timestamps and attempts:
  - `IN_PROGRESS` - Still within time window, not completed
  - `WON` - Completed with correct answer before timer expired
  - `LOST` - Completed without correct answer before timer expired
  - `ABANDONED` - Timer expired OR completed after timer expired

**Methods:**
- `complete()` - Mark session as completed (sets completed_at timestamp)

**Relations:**
- One-to-Many → Attempt (via `attempts` related_name)

**Meta:**
- Ordering: `['-started_at']`
- Indexes:
  - `(user, -started_at)`
  - `(end_at)` - For expired session queries

**Admin Features:**
- List display: ID, user, shortened question, colored status, score, started date
- Filters: started_at, end_at
- Search: user email/username
- Inline: Attempts (read-only)
- Custom Methods:
  - `status_display()` - Shows computed status with color coding (blue=IN_PROGRESS, green=WON, red=LOST, gray=ABANDONED)
  - `question_short()` - Shows shortened bilingual question text (English)

**Design Note:** Status is computed from timestamps, not stored in database. This prevents data inconsistency and provides single source of truth.

---

### 4. Attempt

**Purpose:** Record individual answer attempts within a game session.

**Table:** `quiz_attempt`

**Fields:**
- `game_session` (ForeignKey → GameSession) - Parent game session
- `attempt_number` (PositiveIntegerField) - Attempt sequence (1-6)
- `user_answer` (CharField, max 100) - What the user submitted
- `is_correct` (BooleanField) - Whether answer was correct
- `attempted_at` (DateTimeField, auto) - When attempt was made

**Meta:**
- Ordering: `['attempt_number']`
- Unique Together: `(game_session, attempt_number)`
- Index: `(game_session, attempt_number)`

**Note:** User and Question are inherited from GameSession (no direct FK)

**Admin Features:**
- List display: ID, game session, attempt number, answer, correctness, timestamp
- Filters: is_correct, attempted_at
- Search: user email, user answer
- Also displayed inline in GameSession admin

---

### 5. UserStatistics

**Purpose:** Track user progression level and experience points.

**Table:** `quiz_user_statistics`

**Fields:**
- `user` (OneToOneField → User) - User these stats belong to
- `player_level` (PositiveIntegerField, default: 1) - Game progression level ← **Moved from Profile**
- `experience_points` (PositiveIntegerField, default: 0) - Total XP earned ← **Moved from Profile**
- `created_at` (DateTimeField, auto) - Record creation timestamp
- `updated_at` (DateTimeField, auto) - Last update timestamp

**Properties:** (none)

**Methods:** (none)

**Signal:**
- Auto-created when User is created (via `post_save` signal)

**Meta:**
- Verbose Name: "user statistics"

**Admin Features:**
- List display: user, player_level, experience_points
- Filters: player_level, created_at
- Search: user email/username
- Readonly: created_at, updated_at, user (when editing)
- Ordering: by experience_points (descending)

**Design Note:** Detailed statistics (streak, accuracy, hints, attempt counts) were removed for simplicity in Phase I. These metrics can be calculated on-demand from GameSession and Attempt records when needed.

---

### 6. Trophy

**Purpose:** Define achievements/trophies users can unlock.

**Table:** `quiz_trophy`

**Fields:**
- `code` (CharField, unique, max 50) - Unique identifier (e.g., `FIRST_WIN`, `STREAK_10`)
- `requirement_type` (CharField) - Type of requirement:
  - `LEVEL` - Based on player level
  - `CATEGORY_MASTER` - Based on category mastery
- `name` (CharField, max 100) - Trophy name
- `description` (TextField) - How to unlock this trophy

**Removed Fields:** `icon`, `requirement_value`, `xp_reward`, `is_active`, `order`, `created_at`

**Meta:**
- Ordering: `['name']`

**Admin Features:**
- List display: name, code, requirement_type
- Search: name, code, description
- Ordering: by name

**Design Note:** Trophy model simplified for Phase I MVP. Trophies managed via fixtures. Unlock logic implemented in application code rather than model constraints. Future phases may reintroduce `requirement_value`, `xp_reward`, and `order` fields.

---

### 7. UserTrophy

**Purpose:** Track which trophies each user has unlocked (many-to-many through table).

**Table:** `quiz_user_trophy`

**Fields:**
- `user` (ForeignKey → User) - User who unlocked the trophy
- `trophy` (ForeignKey → Trophy) - Trophy that was unlocked
- `unlocked_at` (DateTimeField, auto) - When trophy was unlocked

**Meta:**
- Ordering: `['-unlocked_at']`
- Unique Together: `(user, trophy)` - Each trophy can only be unlocked once per user
- Index: `(user, -unlocked_at)`

**Admin Features:**
- List display: user, trophy, unlocked date
- Filters: unlocked_at, trophy
- Search: user email/username, trophy name
- Readonly: unlocked_at, user (when editing), trophy (when editing)

---

## Relationships Diagram

```
User (from users app)
 │
 ├──[OneToOne]──> UserStatistics (quiz stats, level, XP)
 │
 ├──[OneToMany]──> GameSession (user's game sessions)
 │                      │
 │                      ├──[ManyToOne]──> Question ──[ManyToOne]──> Category
 │                      │
 │                      └──[OneToMany]──> Attempt (1-6 attempts per session)
 │
 └──[ManyToMany]──> Trophy (via UserTrophy)
```

---

## Internationalization (i18n)

**Approach:** Hybrid - JSONField for content, Django i18n for UI

**Supported Languages:**
- English (en) - Primary
- Traditional Chinese (zh)

### Bilingual Content Storage

**Question Content Fields (JSONField approach):**
- `question_text`, `hint_text`, `explanation` are stored as JSONField
- Format: `{"en": "English text", "zh": "中文文本"}`
- Access via helper methods: `get_question_text(language)`, `get_hint_text(language)`, `get_explanation(language)`
- Allows per-question translations without database migrations
- Content stored directly in database for easy admin editing

**UI Labels (.po file approach):**
- Model field verbose names and help text (via `gettext_lazy`)
- Enum choices (Category names, Difficulty levels, Trophy requirement types, etc.)
- Admin interface labels
- Form field labels
- Template strings

**Translation Workflow:**
1. **For Question Content:** Admin enters JSON: `{"en": "What is...", "zh": "什麼是..."}`
2. **For UI Labels:**
   - Run `python manage.py makemessages -l zh`
   - Edit `christmax/base/locale/zh/LC_MESSAGES/django.po`
   - Run `python manage.py compilemessages`
3. Content displays in user's selected language

**Trade-off:** JSONField for question content provides flexibility and simplicity. UI labels use Django's standard i18n for consistency with the rest of the application.

---

## Migration History

### Current Status: ⚠️ MIGRATION PENDING

**Pending Migration:** `quiz/migrations/0001_initial.py`
- Creates all 7 quiz models with current schema
- GameSession: No `status` field (computed property instead), includes `end_at` field for timer
- Question: JSONField implementation for bilingual content (question_text, hint_text, explanation)
- UserStatistics: Simplified to only level and XP
- Trophy: Simplified to only code, requirement_type, name, description
- Creates indexes for performance optimization
- Sets up unique constraints and foreign key relationships

**Action Required:**
1. Unstage deleted migration: `git reset HEAD christmax/quiz/migrations/0001_initial.py`
2. Generate fresh migration: `poetry run python manage.py makemigrations quiz`
3. Apply migration: `poetry run python manage.py migrate quiz`

### Previous Migrations

### `users/migrations/0002_remove_profile_experience_points_and_more.py` ✅ Applied
- Removed `experience_points` from `users.Profile`
- Removed `player_level` from `users.Profile`

**Note:** These fields now managed in `quiz.UserStatistics`

---

## Database Tables Created

```
quiz_category           - 7 categories
quiz_question          - Questions with code snippets
quiz_game_session      - Active/completed game sessions
quiz_attempt           - Individual answer attempts
quiz_user_statistics   - User stats (level, XP, streaks)
quiz_trophy            - Achievement definitions
quiz_user_trophy       - Unlocked trophies per user
```

---

## Admin Interface

All 7 models are registered in Django admin with:
- ✅ Custom list displays
- ✅ Filters and search functionality
- ✅ Proper fieldsets grouping
- ✅ Read-only timestamp fields
- ✅ Inline displays where appropriate
- ✅ Shortened text display methods
- ✅ Translated field labels

**Access:** `/admin/quiz/`

## Implementation Notes

### Design Decisions

1. **GameSession as Central Hub:** All game state is tracked through GameSession, simplifying the
   data model and making time tracking straightforward.

2. **Category-Driven UI:** Category model includes `icon_class` (FontAwesome) and `prism_language`
   fields to determine the icon displayed in the UI and the syntax highlighting language for code
   snippets. This centralizes UI presentation logic at the category level.

3. **Bilingual Content via JSONField:** Question content (question_text, hint_text, explanation)
   stored as JSONField with language keys (`{"en": "...", "zh": "..."}`). Allows per-question
   translations without schema changes. UI labels still use .po files for consistency with Django
   i18n conventions.

4. **Computed Status Property:** GameSession status is computed from timestamps (started_at, end_at,
   completed_at) and attempt results. No redundant status field stored in database. Single source of
   truth prevents data inconsistency and simplifies logic.

5. **Simplified Attempt Model:** Attempt only links to GameSession (not directly to User/Question),
   reducing redundancy since this information is available via GameSession.

6. **No Wordle Feedback Yet:** The `feedback` field for color-coded Wordle responses is not
   implemented in Phase I. The `is_correct` boolean is sufficient for basic quiz functionality.

7. **Difficulty as Enum:** Using CharField with choices instead of a separate table keeps the model
   simple while still being easily extensible.

8. **Profile Migration:** Moving `player_level` and `experience_points` to `UserStatistics`
   separates game-specific data from general user profile data, following single responsibility
   principle.

9. **Statistics Calculated On-Demand:** UserStatistics only stores level and XP. Detailed stats
    (streaks, accuracy, hints, attempt counts) can be calculated from GameSession/Attempt records
    when needed, avoiding premature optimization and complex update logic.

### Performance Considerations

- Indexes on frequently queried fields (category, difficulty, user, timestamps, end_at)
- Computed status property avoids unnecessary database writes
- JSONField for bilingual content reduces JOIN operations
- Efficient queries through proper related_name usage
- Minimal denormalization (only level and XP) keeps writes simple

### Future Enhancements (Phase II)

- React UI implementation
- Wordle-style color feedback (green/yellow/gray)
- Real-time multiplayer support
- WebSocket for live updates
- Advanced analytics and reporting
- Question difficulty auto-adjustment based on user performance

---

**End of Document**
