# Changelog

## v3.0.0-rc.3 — FollowCore-CAN

- Identify both controller and driver software as FollowCore-CAN.
- Add public support email, Douyin account, and repository information.
- Add explicit product/variant/control-type fields to controller feedback;
  retain receiver compatibility with older reports.
- Retain the S3 rc.2 manual latest-direction handoff fix.
- Replace the controller's previously generated PingFang subsets with renamed
  bitmap subsets derived from OFL-licensed Source Han Sans.
- Identify the driver through its existing standard read-only `100A:00`
  software-version object, without changing PDO mappings or drive identity.
- Publish matching controller/driver artifacts with checksums and compatibility
  metadata. Motion algorithms and safety thresholds are not changed here.

Status: release candidate. See each release for actual validation and deployment
evidence; do not infer mechanical or long-term acceptance from build success.
