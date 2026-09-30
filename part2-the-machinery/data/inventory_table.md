| Binary | Inode / Hardlink Type | Runtime | Size | Core Responsibility |
|---|---|---|---|---|
| aftership | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.2 MB | aftership connector CLI |
| asana | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | asana connector CLI |
| authdc | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Auth daemon client (multicall applet) |
| box-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.7 MB | box cli connector CLI |
| browser-broker | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 17.8 MB | Long-running broker routing browser sessions to leased VMVM browsers (SO_PEERCRED auth) |
| browser-service | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Browser service (multicall applet) |
| calendly | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.7 MB | calendly connector CLI |
| canva | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.6 MB | canva connector CLI |
| device-data | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Device data (multicall applet) |
| dropbox | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.5 MB | dropbox connector CLI |
| duffel | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.3 MB | duffel connector CLI |
| edits | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Edits capability (multicall applet) |
| etsy-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | etsy cli connector CLI |
| evernote | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.3 MB | evernote connector CLI |
| facebook-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 16.5 MB | facebook cli connector CLI |
| feature-request | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Feature-request/feedback (multicall applet) |
| figma | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | figma connector CLI |
| flightaware | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.2 MB | flightaware connector CLI |
| function-health | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.8 MB | Function Health FHIR API helper CLI |
| genui-display-render | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 17.4 MB | Generate/present component-based GenUI wearable cards |
| geocode | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Geocoding (multicall applet) |
| ghl | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.7 MB | ghl connector CLI |
| github | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.3 MB | github connector CLI |
| granola-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.9 MB | granola cli connector CLI |
| hatch | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 340.3 MB | Daemon service binary (356.9 MB; the Jarvis/Hatch daemon; links libelf+libz) |
| hatch-browser-lease-helper | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 7.3 MB | Socket-activated root relay: broker lease ops -> stefi-proxy + viewer bind-mount |
| hatch-connector-output | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 0.5 MB | Connector output helper (outlier: minimal dynamic deps, no ld-linux NEEDED) |
| hatch-doctor | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.8 MB | Deterministic Hatch runtime state checks |
| hatch-execd | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 8.4 MB | Socket-activated exec daemon (requires --socket or systemd LISTEN_FDS; links libelf+libz) |
| hatch-healthd | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 7.9 MB | Health daemon (takes --daemon-metrics-socket) |
| hatch-multicall | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | hatch multicall connector CLI |
| hatch-rescue | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.9 MB | Rescue agent (http-api, systemctl, ws sockets) |
| hatch-rescue-systemctl | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 2.2 MB | Rescue systemctl shim (2.3 MB) |
| hatch-rescuectl | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 7.7 MB | Rescue-owned operations helper |
| hatch-slide-style | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 9.9 MB | Resolve slide deck StylePlan (archetype/theme/palette/fonts) |
| hatch-vault | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 9.9 MB | Vault client (talks to /run/hatch/vault/*.sock, vault-encrypt, vault-hmac) |
| hatch-ws-client | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.8 MB | Minimal websocket client for Jarvis daemon RPCs |
| hatch-zeitgeist | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.4 MB | Meta 1P social search (Instagram/Threads/Facebook) |
| hatch_gws_auth | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.2 MB | Google Workspace auth helper |
| hatch_gws_cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 14.4 MB | Google Workspace CLI |
| hatch_messenger_cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.0 MB | Messenger CLI |
| health-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 22.3 MB | Health data CLI |
| healthex | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.6 MB | Health exchange helper CLI |
| healthkit-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 14.1 MB | Apple HealthKit CLI |
| image-search | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Image search (multicall applet) |
| ingress-rev-proxy | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.2 MB | Internet-facing ingress reverse proxy with Noise_XX encryption |
| instagram-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 25.1 MB | instagram cli connector CLI |
| instagram-messages-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.8 MB | instagram messages cli connector CLI |
| klaviyo | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.5 MB | klaviyo connector CLI |
| linear | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.5 MB | linear connector CLI |
| local-search | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.1 MB | Local search CLI |
| lovable | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | lovable connector CLI |
| mcp-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.2 MB | MCP client CLI |
| media-generation | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Media generation (multicall applet) |
| media-library | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Media library (multicall applet) |
| meta-ads-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 19.3 MB | meta ads cli connector CLI |
| meta-catalog-search | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.2 MB | Meta catalog search CLI |
| muse-mail | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Muse mail (multicall applet) |
| native-comms-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 9.9 MB | Native communications CLI (calls/texts) |
| notion-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.9 MB | notion cli connector CLI |
| nutrition-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 0.4 MB | Nutrition helper CLI (smallest binary, 0.4 MB, no libm) |
| onepassword | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.0 MB | onepassword connector CLI |
| opentable | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.1 MB | opentable connector CLI |
| outlook-calendar | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.9 MB | outlook calendar connector CLI |
| outlook-contacts | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.9 MB | outlook contacts connector CLI |
| outlook-mail | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.1 MB | outlook mail connector CLI |
| peloton | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.6 MB | peloton connector CLI |
| philips-hue | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.7 MB | philips hue connector CLI |
| places | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.0 MB | places connector CLI |
| plaid | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.2 MB | plaid connector CLI |
| printify | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.8 MB | printify connector CLI |
| privsep-test-fully-isolated | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Privsep isolation self-test (multicall applet) |
| quickbooks | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 16.3 MB | quickbooks connector CLI |
| remote-storage | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.9 MB | Remote file storage CLI |
| replit | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.3 MB | replit connector CLI |
| save-to-spotify | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.7 MB | save to spotify connector CLI |
| share | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Share helper (multicall applet) |
| shop-wallet-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.6 MB | shop wallet cli connector CLI |
| shopify | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.5 MB | shopify connector CLI |
| shopify-ucp-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 15.5 MB | shopify ucp cli connector CLI |
| shopping | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Shopping (multicall applet) |
| slack | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | slack connector CLI |
| spawnd | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 17.1 MB | Jarvis runtime installer engine (lifecycle, RV graft, privsep workers, eBPF gates; links libelf+libz) |
| spotify-api | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.8 MB | spotify api connector CLI |
| stripe | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | stripe connector CLI |
| stripe-link | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | stripe link connector CLI |
| subscription-status | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Subscription status (multicall applet) |
| tailscale | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 10.4 MB | Tailscale CLI wrapper |
| tessie-api | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.5 MB | tessie api connector CLI |
| threads-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 13.3 MB | threads cli connector CLI |
| threads-messages-cli | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.7 MB | threads messages cli connector CLI |
| ticketmaster | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.6 MB | ticketmaster connector CLI |
| todoist | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | todoist connector CLI |
| tts | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Text-to-speech (multicall applet) |
| vercel | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | vercel connector CLI |
| wearables-display | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 14.6 MB | wearables display connector CLI |
| web-search | hardlink (multicall, inode 1062, 17 names) | Rust (rustc 1.97.1) | 28.3 MB | Web search (multicall applet) |
| withings | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 12.9 MB | withings connector CLI |
| zapier | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.3 MB | zapier connector CLI |
| zoom | hardlink pair (nlink=2) | Rust (rustc 1.97.1) | 11.4 MB | zoom connector CLI |