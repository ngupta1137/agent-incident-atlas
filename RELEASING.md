# Releasing and tracking on Zenodo

Every release of the Atlas is archived on Zenodo, which gives it a permanent DOI that people can cite. Zenodo's GitHub integration does the archiving when you publish a GitHub release. Nothing is archived until you do the one-time setup below, and the order matters.

Zenodo issues two kinds of DOI for a project:

- A **concept DOI** that always resolves to the latest version. Use this when citing the project in general.
- A **version DOI** for each release. Use this when citing an exact version of the data.

## One-time setup

1. Publish the repository on GitHub as a **public** repository. Zenodo cannot archive private repositories.
2. Replace the `ngupta1137` placeholder with your GitHub username or organization in `CITATION.cff`, `README.md`, and `.zenodo.json` if present. For example:
   ```bash
   grep -rl ngupta1137 . --include="*.md" --include="*.cff" --include="*.json" | xargs sed -i 's/ngupta1137/your-github-name/g'
   ```
3. Create or sign in to a Zenodo account at zenodo.org using **Log in with GitHub**.
4. In Zenodo, open your account menu, choose **GitHub**, and click **Sync now**. Find `agent-incident-atlas` and switch its toggle **on**. This must happen **before** you publish the release, or Zenodo will not archive it.
5. Optional but recommended: add your ORCID iD to the `authors` entry in `CITATION.cff` and to `creators` in `.zenodo.json` (`"orcid": "0000-0000-0000-0000"`), so the record is linked to your researcher profile.
6. Optional: rehearse the whole flow at sandbox.zenodo.org first. It is a separate site with a separate account, and nothing there is permanent.

## Releasing a version

1. Update the data and docs. Run:
   ```bash
   python scripts/validate.py
   python scripts/build_exports.py
   ```
2. Bump the version in `CITATION.cff` (`version` and `date-released`) and in `.zenodo.json` (`version`). Add an entry at the top of `CHANGELOG.md`.
3. Check consistency:
   ```bash
   python scripts/check_release.py --strict
   ```
4. Commit and push to `main`. Wait for the `validate` workflow to pass.
5. Tag and publish the release on GitHub:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
   Then on GitHub go to **Releases**, **Draft a new release**, choose the tag, add short notes (copy from the changelog), and click **Publish release**. A tag alone does not trigger Zenodo. The published release does.
6. Within a few minutes Zenodo creates the record. Open it from your Zenodo **Uploads** page and check the title, description, creators, license, and version. Zenodo reads `.zenodo.json` first. If that file is present it takes priority over `CITATION.cff` for the record's metadata, so keep the two consistent. Fix any problem by editing the record on Zenodo, or by correcting the files and publishing a new release.

## After the first release

The DOI does not exist until Zenodo archives the first release, so the first release cannot contain it. Do this afterward:

1. Copy the **concept DOI** from the Zenodo record (the one labeled "Cite all versions").
2. Add it to `CITATION.cff` as `doi: "10.5281/zenodo.NNNNNNN"` and replace `XXXXXXX` in the BibTeX block in `README.md`. Add the Zenodo DOI badge from the record's page if you want one.
3. Commit these changes. They ship with the next release (for example 0.1.1). That is normal and expected.

## Routine after that

Repeat the release steps for every version. Each new GitHub release creates a new version under the same concept DOI, so citations to the project never break.

## Notes

- **License field.** `.zenodo.json` declares `cc-by-4.0` because the dataset is the primary object. The MIT license for code is stated in the record description and in `LICENSE-NOTE.md`. Check how the license appears on the draft Zenodo record after the first release.
- **Seed data.** The `.zenodo.json` description states that version 0.1.0 contains illustrative seed records only. Keep this statement until the dataset contains real contributions, and revise it deliberately when it does.
- **Do not delete a published version.** Zenodo records are permanent. If a record contains something that should not be public, contact Zenodo support and publish a corrected version.
- **Related outputs.** Each other repository you publish (a book companion repository, templates, checklists) should get its own Zenodo record, and the records can reference one another through the "Related works" field on Zenodo. This keeps one list of dated, citable outputs.
