# Service options

Options represent supported versions or deployment variants of a service.

A service can expose multiple options, and one of them can be marked as the default. Options can also carry an End of Life (EOL) date to show when upstream support ends.

Service options are defined under the [`options` section](template.md#options) in a service template.

## EOL flags

`EOL` means the selected service option has reached its end-of-life date. The service may still run, but upstream support
for that version has ended and you should plan to move to a supported option.

Wodby shows EOL flags in a few places:

- service version selectors and app-service version rows, when the selected version is EOL
- stack pages and stack lists, when an enabled stack service defaults to an EOL version
- app instance pages and app instance lists, when an enabled app service currently uses an EOL version

EOL checks use the latest service revision metadata available to Wodby. If a stack service or app service still points
to an older service revision, the dashboard can still mark the selected version as EOL, but the older revision may not
show the newest EOL date metadata or the newest non-EOL replacement versions in its version selector.

Update the stack service to the latest service revision before reviewing exact EOL dates or choosing a newer non-EOL
option. For app instances, publish the updated stack revision and upgrade the app instance; if needed, enable
`Update versions to default` during the app instance stack upgrade or change the app-service version afterward.
