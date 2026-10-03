# Homing pack: `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-input-stack-device-channel-and-bindings.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 007A1080 (21 B, extent 007A1080-007A1095)

Entered from (direct sites whose caller this page cites): `00198E80` + 0x3A (call; `00198E80` is cited on this page)
Other direct sites: none

Host context: "ontrol_UpdateDeviceFeedbackOutput' '0035F590' → 'InputFeedbackBridge_DispatchTwoBytePair' '008628F0' → 'InputFeedback_DispatchViaManagerGate' '001E1120' → 'InputManager_DispatchFeedbackToDeviceById' '00198E80'. **The dependency is one-directional:** a direct-call walk from 'InputManager_*' visits 357 functions to depth 8 and reaches no 'InputControl_*' body, while 'InputControl_*' reaches 'InputManager_*' in three hops. So 'InputControl"

```
007A1080  mov      byte ptr [rcx + 0x98], dl
007A1086  mov      byte ptr [rcx + 0x99], r8b
007A108D  mov      byte ptr [rcx + 0x9a], 1
007A1094  ret      
```
