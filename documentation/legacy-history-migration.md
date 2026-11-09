# Vega Strike Assets-Production Legacy History Migration

This document details the mapping, reconstruction, and verification of historical release branches and legacy release tags for the **Assets-Production** repository (*Vega Strike: Upon the Coldest Sea* game data and assets).

---

## 1. Background & Scope

During the CVS and early Subversion eras (2001–2008), the Vega Strike project maintained game engine code and asset trees together in a monolithic repository on SourceForge:
* **Repository URL:** `https://svn.code.sf.net/p/vegastrike/code`
* **Repository UUID:** `9476613a-4e0a-0410-bcee-947800e9c4d1`

In this era, asset data resided within `trunk/data` (for versions 0.1.x–0.3.x) and later `trunk/data4.x` (for versions 0.4.x–0.5.0). When the project migrated from Subversion to Git, the asset history was migrated into `Assets-Production`. However, historical release tags predating GitHub were preserved only as manufactured tag commits or remained in the Subversion repository's `/tags` path.

This migration reconstructs sequential release branches (`0.1.x`, `0.2.x`, `0.3.x`, `0.4.x`) and standardizes all legacy asset release tags under the `legacy_<tag_name>` naming scheme.

---

## 2. Release Line & Tag Mapping Table

| Series | Tag Name | Base Anchor Commit | Tree SHA | SVN Tag Path | Original Author | Historical Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0.1.x** | `legacy_betareleasecandidate102901` | `a5e84968` | `f879cf1b` | CVS Tag | Daniel Horn | 2001-10-29 |
| | `legacy_vegastrike_0.1.0` | `ed8fd1be` | `ed8fd1be` | CVS Tag | Daniel Horn | 2001-11-07 |
| | `legacy_vegastrike_0.1.3` | `1f39f60d` | `1f39f60d` | CVS Tag | Daniel Horn | 2002-01-15 |
| | `legacy_after_data_removal_stage1` | `1c8dbe4c` | `45c20130` | `tags/after_data_removal_stage1` | Alexander Rawass | 2002-01-17 |
| | `legacy_vegastrike_snapshot_020117` | `9069797b` | `42d0dbce` | `tags/vegastrike_snapshot_020117_data` | Alexander Rawass | 2002-01-18 |
| **0.2.x** | `legacy_release-0-2-0` | `6789e4ba` | `d390634b` | `tags/release-0-2-0` | Daniel Horn | 2002-02-19 |
| | `legacy_vegastrike_0_2_1` | `5ac77a29` | `283ea4be` | CVS Tag | Daniel Horn | 2002-03-11 |
| | `legacy_stable_050102` | `354a5e6c` | `49ff31d5` | CVS Tag | Daniel Horn | 2002-05-01 |
| | `legacy_vegastrike_0_2_9` | `230c437c` | `e32a6568` | `tags/vegastrike_0_2_9/data` | Daniel Horn | 2002-06-27 |
| | `legacy_vegastrike_0_2_9_2` | `910b5ca4` | `f5ec2d05` | `tags/vegastrike_0_2_9_2/data` | Daniel Horn | 2002-07-01 |
| | `legacy_vegastrike_0_2_9_3` | `5a4d0b5a` | `4e4f54ab` | `tags/vegastrike_0_2_9_3/data` | Daniel Horn | 2002-08-30 |
| | `legacy_vegastrike_0_2_9_4` | `5a4d0b5a` | `034c95c0` | `tags/vegastrike_0_2_9_4/data` | Daniel Horn | 2002-08-30 |
| **0.3.x** | `legacy_vegastrike_0_3_0` | `b6786e0f` | `ddf50003` | `tags/vegastrike_0_3_0/data` | Daniel Horn | 2003-01-07 |
| | `legacy_vegastrike_0_3_1` | `40e65dc6` | `67e59208` | `tags/vegastrike_0_3_1/data` | Daniel Horn | 2003-01-10 |
| | `legacy_vegastrike_0_3_3` | `e8746815` | `95a70313` | CVS Tag | Daniel Horn | 2003-01-24 |
| | `legacy_vegastrike_0_3_9` | `d59f2987` | `bf700eec` | `tags/vegastrike_0_3_9/data` | Daniel Horn | 2003-06-30 |
| **0.4.x** | `legacy_vegastrike_0_4_0` | `811c6471` | `636893e4` | `tags/vegastrike_0_4_0/data4.x` | Daniel Horn | 2003-10-01 |
| | `legacy_vegastrike_0_4_1` | `e4bac199` | `d123034a` | `tags/vegastrike_0_4_1/data4.x` | Daniel Horn | 2003-10-24 |
| | `legacy_vegastrike_0_4_2` | `3b7194e8` | `6ea9066b` | `tags/vegastrike_0_4_2/data4.x` | Daniel Horn | 2004-09-29 |
| | `legacy_vegastrike_0_4_3` | `c6873c44` | `380ac1c3` | `tags/vegastrike_0_4_3/data4.x` | Daniel Horn | 2005-02-12 |
| **0.5.x** | `legacy_0.5.0` | `cb972649` | `454305ea` | `tags/0.5.0/data4.x` | ace123 | 2008-05-08 |
| | `legacy_vegastrike_0_5_1_beta1` | `96df17a2` | `d013a239` | `tags/vegastrike_0_5_1_beta1/data` | klaussfreire | 2011-03-09 |
| | `legacy_vegastrike_0_5_1_beta2` | `aeb92a18` | `3d41eaa4` | `tags/vegastrike_0_5_1_beta2/data` | klaussfreire | 2012-01-30 |
| | `legacy_vegastrike_0_5_1_r1` | `0ee8392f` | `d8e67407` | `tags/vegastrike_0_5_1_r1/data` | klaussfreire | 2012-04-01 |
| | `legacy_0.5.2alpha-archive` | `ee045171` | `e776f7ad` | `tags/0.5.2alpha-archive/data` | pyramid3d | 2020-02-06 |

---

## 3. Migration Methodology

1. **Subversion Tag Trees**: The actual release data trees in Subversion resided within the `data/` or `data4.x/` directories of each tag in the Subversion repository.
2. **Plumbing Operations**: Using `git write-tree` via an isolated temporary index file (`tempfile.gettempdir()`), exact Git tree objects were synthesized from the Subversion tag checkouts.
3. **Commit Chaining**: Sequential release branches (`0.1.x`, `0.2.x`, `0.3.x`, `0.4.x`) were created using `git commit-tree` to preserve parentage while maintaining historical authorship and committer timestamps.
4. **Annotated Legacy Tags**: Tags were created using `git tag -a -f --no-sign` under the `legacy_*` prefix to prevent collision with modern GitHub release tags.

---

## 4. Automation Tool

The migration is automated via [`script/migrate_legacy_svn_history.py`](../script/migrate_legacy_svn_history.py).

### Usage:
```bash
# Dry run verification
python3 script/migrate_legacy_svn_history.py --svn-dir /path/to/svn/vegastrike-code

# Execute migration
python3 script/migrate_legacy_svn_history.py --svn-dir /path/to/svn/vegastrike-code --execute
```
