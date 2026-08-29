# Sweep Food Database Notes

`DATABASE.txt` is the canonical MVP data contract. It is the source of truth for tables, fields, enums, and relationships. Redis stores only short-lived OTP challenges, rate limits, distributed locks, and worker coordination.

## Data Ownership and Authentication

- All IDs are UUIDs. All persisted timestamps are UTC. Expiration notifications use the fixed product timezone `Asia/Ho_Chi_Minh`; timezones are not stored per user in this MVP.
- A user-owned record must be authorized through its direct `user_id` or an owned parent record. Admin users are created by the Python seed script; no public admin CRUD endpoint exists.
- `users.phone_e164` is unique. `users.email` is unique when present, and email OTP is allowed only after `email_verified_at` is set.
- OTP plaintext, provider credentials, and raw OCR/ASR/barcode input or output are never persisted.
- `auth_sessions.refresh_token_hash` is the only stored refresh-token representation. On refresh-token reuse, revoke sessions sharing the token family.

## Catalog and Seed Rules

- Ingredient and recipe seed data is upserted by a documented deterministic natural key, such as normalized ingredient name plus category and normalized recipe name. The seed file must not create duplicate catalog rows when rerun.
- `ingredient_aliases.normalized_alias` is unique. It maps a user/provider synonym to exactly one master ingredient.
- A shelf-life rule targets exactly one master ingredient or one category. Ingredient-level rules take precedence over category-level rules. The seed data must not contain duplicate target/storage-mode rules.
- `recipe_ingredients.required_quantity` and `recipes.default_servings` must be greater than zero.
- Unit compatibility is inferred from `MeasurementUnit`: `GRAM`/`KG` are mass; `ML`/`LITER` are volume; `PIECE`/`PACK`/`OTHER` do not have automatic cross-unit conversion.

## Inventory, FEFO, and Ledger Rules

- Each `inventory_batches` row is one real batch. Purchases or packages with different expiration dates must stay separate.
- A batch requires exactly one of `master_ingredient_id` and `custom_name`.
- `initial_quantity > 0` and `current_quantity >= 0`. A zero balance becomes `DEPLETED`; discard and archive use their explicit status values.
- A manufacturer date takes precedence and sets `expiration_source = MANUFACTURER`. Otherwise the backend estimates a date using the matching shelf-life rule and records `ESTIMATED`; user edits use `USER_OVERRIDE`; unavailable dates use `UNKNOWN` with null `expires_at`.
- Freshness is computed at query time: expired, expiring soon, safe, or unknown. It is not a stored source-of-truth field.
- FEFO selects active, non-expired, unit-compatible batches by `expires_at`, then `created_at`, with null expiration dates last. Completion revalidates and locks selected batches.
- Every quantity mutation is transactional and creates an immutable `inventory_ledger_entries` record. `quantity_after = quantity_before + quantity_delta` and the batch balance must match the completed mutation.
- `idempotency_key` is unique within its user/operation scope. A retry must not duplicate a cooking consumption or ledger entry.
- A leftover creates a `COOKED_FOOD` batch with `source = LEFTOVER`, linked to its completed cooking session, and a `LEFTOVER_CREATED` ledger entry.

## Recommendations, Plans, Cooking, and Shopping

- `recommendation_items.rank` is unique within a recommendation run. The run records the provider and optional model version; MVP uses `RULE_BASED_MVP` and later supports XGBoost or LightGBM.
- Recommendation interaction events are intentionally not persisted in MVP. Future model training may add them in a separate migration.
- A meal-plan item date must fall within its parent plan range. `(meal_plan_id, planned_for, meal_slot)` is unique.
- Cooking completion creates exact `cooking_consumptions`, matching `COOKING_CONSUMPTION` ledger records, and updates the cooking session atomically.
- A shopping-list item requires a master ingredient or custom name. `source_metadata` keeps the generated recipe context; manually edited values remain user-owned.
- `(user_id, recipe_id)` is unique in `favorite_recipes`. Favorite-menu recipes use creation order; ordering is not stored separately in MVP.

## Devices and Notifications

- Encrypt FCM tokens and use the hash only for lookup/deduplication. A permanent FCM failure disables the corresponding device; notification history remains intact.
- Each user has at most one `user_notification_preferences` row. A null `warning_days` uses the category/storage default.
- `notifications.deduplication_key` is unique and derives from batch, notification type, and effective date in `Asia/Ho_Chi_Minh`.
- Notification delivery failures update retry/delivery state only; they never roll back inventory or cooking transactions.

## Required Indexes

- Unique `users(phone_e164)` and non-null `users(email)`.
- `auth_sessions(user_id, expires_at)` and `auth_sessions(token_family_id)`.
- `master_ingredients(category_id)`, unique `ingredient_aliases(normalized_alias)`, and shelf-life lookup by ingredient/category plus storage mode.
- `recipe_ingredients(recipe_id)` and `recipe_ingredients(master_ingredient_id)`.
- `inventory_batches(user_id, status, expires_at, created_at)` for FEFO, plus user/ingredient and user/storage-mode filtering.
- `inventory_ledger_entries(inventory_batch_id, created_at)` and user/time history.
- Recommendation run/item indexes by user/run/recipe and creation time.
- Meal-plan/user/date, cooking-session/user/status/time, consumption/session/batch, shopping-list/user/status, and shopping-item/list indexes.
- Unique favorite recipe pair, favorite-menu item pair, device token hash, notification preference user, notification deduplication key, and notification user/status/created-time indexes.

## Non-persisting MVP Extraction

ASR (LiveKit plus an external AI provider), OCR, invoice extraction, and barcode lookup return their normalized result only. They do not create inventory, catalog, ledger, recommendation-interaction, or raw-media records in this MVP.
