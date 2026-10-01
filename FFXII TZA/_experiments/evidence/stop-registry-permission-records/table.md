| id | raised by | flag | A `+0` | B `+0` | 1 movement | 2 script | 3 | 4 | 5 animation | 6 unit `+0x004` b5 | 7 unit flag b36 | managers | global bits cleared |
|---:|---|:-:|---|---|---|---|---|---|---|---|---|:-:|---|
| 0 | UI requests 1/4/20 | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 1 | *no start site* | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 2 | UI requests 3/24 | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 3 | *no start site* | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 4 | field hold mode 1; boot | 0 | `00000024F9040707` | `00001F2B0B001F1F` | T3 T127 R H | T3 T127 R H | T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A25,26 B26 A36 B36 A39 |
| 4 | field hold mode 1; boot | 1 | `00000024F9040505` | `00001F2A09001F1F` | P T3 T127 R H | P T3 T127 R H | P T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A25,26 B25,26 B32 A36 B36 A39 |
| 5 | field hold mode 0 | any | `00000034EB000000` | `00001F3A0B00101F` | all | all | all | R H | F P T127 T0 R H | all | all | 1 | A26 B26 B32 A39 |
| 6 | event script takes actor; `talkfadeout` | 0 | `00000004DB040707` | `00001F0B0B001F1F` | T3 T127 R H | T3 T127 R H | T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A26 B26 A29 A36,37 B36,37 A39 |
| 6 | event script takes actor; `talkfadeout` | 1 | `00000004DB040505` | `00001F0A0B001F1F` | P T3 T127 R H | P T3 T127 R H | P T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A26 B26 A29 B32 A36,37 B36,37 A39 |
| 7 | field hold mode 2 | 0 | `00000024F9044307` | `00001F2B0B005F1F` | T3 T127 R H | T3 T127 T0 R | T3 T127 T0 R | R H | R | F P T3 T127 R H | all | 1 | A25,26 B26 A36 B36 A39 |
| 7 | field hold mode 2 | 1 | `00000024F9044105` | `00001F2A09005F1F` | P T3 T127 R H | P T3 T127 T0 R | P T3 T127 T0 R | R H | R | F P T3 T127 R H | all | 1 | A25,26 B25,26 B32 A36 B36 A39 |
| 8 | *no start site* | any | `00000030BD000060` | `00001F3209001F7F` | F P T3 T127 T0 | all | all | — | R H | all | all | 1 | A25 B25,26 A30 B32 B35 A39 |
| 9 | *no start site* | any | `00000030BD000060` | `00001F3209001F7F` | F P T3 T127 T0 | all | all | — | R H | all | all | 1 | A25 B25,26 A30 B32 B35 A39 |
| 10 | `settimestopmagic`; target cursor | any | `00000030BF7F6060` | `00001F320B001F1F` | F P T3 T127 T0 | F P T3 T127 T0 | F P T3 T127 T0 | R H | R H | — | all | 1 | B26 A30 B32 B35 A39 |
| 11 | `seteventtimestop` | any | `0000002011000000` | `00001F2A0B001F1F` | all | all | all | R H | R H | all | all | 3 | A25,26,27 B26 A29 A30 B32 A36 B36 A39 |
| 12 | `settutorial00timestop` | any | `00000024DD001F01` | `00001F3A0B1F1F1F` | P T3 T127 T0 R H | R H | R H | R H | R H | all | R H | 1 | A25 B26 A29 B32 A36 A39 |
| 13 | full-screen menus | any | `FFFFFFFFD5FFE0FF` | `FFFFFDFDFDFFFFFF` | — | F P T3 T127 T0 | F P T3 T127 T0 | — | — | — | — | 1 | A25,27 B25 A29 B33 B41 |
| 14 | *no start site* | any | `00000000BD000000` | `00001F0A09001F1F` | all | all | all | R H | R H | all | all | 1 | A25 B25,26 A30 B32 A36,37 B36,37 A39 |
| 15 | `002E2240` | any | `00000034D4000000` | `0000003A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 B40,41,42,43,44 |
| 16 | mask verbs | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | A24 B24 |
| 17 | `ucon` | any | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | — | — | — | — | — | F P | F P | 1 | — |
| 18 | `0025C830` | any | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | — | — | — | — | — | F P | F P | 1 | — |
| 19 | definition load | any | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | — | — | — | — | — | F P | F P | 1 | — |
| 20 | *no start site* | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | A24 B24 |
| 21 | *no start site* | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | A24 B24 |
| 22 | `0035C7B0` (game-over route) | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 23 | `…dispdenystatus` | any | `FFFFFFFFFFFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | B24 |
| 24 | `…ctrldenystatus` | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFFFFFFFF` | — | — | — | — | — | — | — | 1 | A24 |
| 25 | `…dispdenystatus_by_menu` | any | `FFFFFFFFFFFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | B24 |
| 26 | `…ctrldenystatus_by_menu` | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFFFFFFFF` | — | — | — | — | — | — | — | 1 | A24 |
| 27 | `skipexec` | any | `FFFFFFFFFFFFFFFF` | `FFFFE2FFFFFFFFFF` | — | — | — | — | — | — | — | 1 | B40,42,43,44 |
