lodc 003b5980: 4053             push rbx
lodc 003b5982: 4883ec40         sub rsp, 0x40
lodc 003b5986: 0fb6d1           movzx edx, cl
lodc 003b5989: 4869dae0000000   imul rbx, rdx, 0xe0
lodc 003b5990: 8bc1             mov eax, ecx
lodc 003b5992: 48031d8fab7802   add rbx, qword ptr [rip + 0x278ab8f]
lodc 003b5999: 394b10           cmp dword ptr [rbx + 0x10], ecx
lodc 003b599c: 740e             je 0x3b59ac
lodc 003b599e: f30f100502629301 movss xmm0, dword ptr [rip + 0x1936202]
lodc 003b59a6: 4883c440         add rsp, 0x40
lodc 003b59aa: 5b               pop rbx
lodc 003b59ab: c3               ret 
lodc 003b59ac: 0fb74304         movzx eax, word ptr [rbx + 4]
lodc 003b59b0: 6683f8ff         cmp ax, -1
lodc 003b59b4: 74e8             je 0x3b599e
lodc 003b59b6: 480fbfc0         movsx rax, ax
lodc 003b59ba: 4869c840070000   imul rcx, rax, 0x740
lodc 003b59c1: 33c0             xor eax, eax
lodc 003b59c3: 48030d5e15f101   add rcx, qword ptr [rip + 0x1f1155e]
lodc 003b59ca: 398184020000     cmp dword ptr [rcx + 0x284], eax
lodc 003b59d0: 480f44c8         cmove rcx, rax
lodc 003b59d4: 4885c9           test rcx, rcx
lodc 003b59d7: 74c5             je 0x3b599e
lodc 003b59d9: 0fb7533c         movzx edx, word ptr [rbx + 0x3c]
lodc 003b59dd: 48897c2458       mov qword ptr [rsp + 0x58], rdi
lodc 003b59e2: e809c60600       call 0x421ff0
lodc 003b59e7: 488bf8           mov rdi, rax
lodc 003b59ea: 4885c0           test rax, rax
lodc 003b59ed: 0f84ef010000     je 0x3b5be2
lodc 003b59f3: 0fb74304         movzx eax, word ptr [rbx + 4]
lodc 003b59f7: 6683f8ff         cmp ax, -1
lodc 003b59fb: 0f84e1010000     je 0x3b5be2
lodc 003b5a01: 480fbfc0         movsx rax, ax
lodc 003b5a05: 4869c840070000   imul rcx, rax, 0x740
lodc 003b5a0c: 48030d1515f101   add rcx, qword ptr [rip + 0x1f11515]
lodc 003b5a13: 0f84c9010000     je 0x3b5be2
lodc 003b5a19: 83b98402000000   cmp dword ptr [rcx + 0x284], 0
lodc 003b5a20: 0f84bc010000     je 0x3b5be2
lodc 003b5a26: e845150300       call 0x3e6f70
lodc 003b5a2b: 4885c0           test rax, rax
lodc 003b5a2e: 0f84ae010000     je 0x3b5be2
lodc 003b5a34: f30f104020       movss xmm0, dword ptr [rax + 0x20]
lodc 003b5a39: f30f104824       movss xmm1, dword ptr [rax + 0x24]
lodc 003b5a3e: 0f2815db847302   movaps xmm2, xmmword ptr [rip + 0x27384db]
lodc 003b5a45: f30f11442420     movss dword ptr [rsp + 0x20], xmm0
lodc 003b5a4b: f30f10402c       movss xmm0, dword ptr [rax + 0x2c]
lodc 003b5a50: f30f114c2424     movss dword ptr [rsp + 0x24], xmm1
lodc 003b5a56: f30f1144242c     movss dword ptr [rsp + 0x2c], xmm0
lodc 003b5a5c: 0f28442420       movaps xmm0, xmmword ptr [rsp + 0x20]
lodc 003b5a61: 0f11154837f201   movups xmmword ptr [rip + 0x1f23748], xmm2
lodc 003b5a68: 0f104f30         movups xmm1, xmmword ptr [rdi + 0x30]
lodc 003b5a6c: 0f11055d37f201   movups xmmword ptr [rip + 0x1f2375d], xmm0
lodc 003b5a73: 0f110d4637f201   movups xmmword ptr [rip + 0x1f23746], xmm1
lodc 003b5a7a: f30f10054237f201 movss xmm0, dword ptr [rip + 0x1f23742]
lodc 003b5a82: f30f5cca         subss xmm1, xmm2
lodc 003b5a86: 0f29742430       movaps xmmword ptr [rsp + 0x30], xmm6
lodc 003b5a8b: f30f110d2d37f201 movss dword ptr [rip + 0x1f2372d], xmm1
lodc 003b5a93: 0f28ca           movaps xmm1, xmm2
lodc 003b5a96: 0fc6ca55         shufps xmm1, xmm2, 0x55
lodc 003b5a9a: f30f5cc1         subss xmm0, xmm1
lodc 003b5a9e: 0f28ca           movaps xmm1, xmm2
lodc 003b5aa1: 0fc6caaa         shufps xmm1, xmm2, 0xaa
lodc 003b5aa5: 0fc6d2ff         shufps xmm2, xmm2, 0xff
lodc 003b5aa9: f30f11051337f201 movss dword ptr [rip + 0x1f23713], xmm0
lodc 003b5ab1: f30f10050f37f201 movss xmm0, dword ptr [rip + 0x1f2370f]
lodc 003b5ab9: f30f5cc1         subss xmm0, xmm1
lodc 003b5abd: f30f11050337f201 movss dword ptr [rip + 0x1f23703], xmm0
lodc 003b5ac5: f30f1005ff36f201 movss xmm0, dword ptr [rip + 0x1f236ff]
lodc 003b5acd: f30f5cc2         subss xmm0, xmm2
lodc 003b5ad1: f30f1105f336f201 movss dword ptr [rip + 0x1f236f3], xmm0
lodc 003b5ad9: e8a282fbff       call 0x36dd80
lodc 003b5ade: f30f1005de36f201 movss xmm0, dword ptr [rip + 0x1f236de]
lodc 003b5ae6: f30f10350e39b401 movss xmm6, dword ptr [rip + 0x1b4390e]
lodc 003b5aee: f30f101dd236f201 movss xmm3, dword ptr [rip + 0x1f236d2]
lodc 003b5af6: 0f28ce           movaps xmm1, xmm6
lodc 003b5af9: f30f1015bf36f201 movss xmm2, dword ptr [rip + 0x1f236bf]
lodc 003b5b01: f30f59c0         mulss xmm0, xmm0
lodc 003b5b05: f30f59db         mulss xmm3, xmm3
lodc 003b5b09: f30f59c8         mulss xmm1, xmm0
lodc 003b5b0d: f30f1105af36f201 movss dword ptr [rip + 0x1f236af], xmm0
lodc 003b5b15: 0f28c6           movaps xmm0, xmm6
lodc 003b5b18: f30f59d2         mulss xmm2, xmm2
lodc 003b5b1c: f30f111da436f201 movss dword ptr [rip + 0x1f236a4], xmm3
lodc 003b5b24: f30f59c2         mulss xmm0, xmm2
lodc 003b5b28: f30f58c8         addss xmm1, xmm0
lodc 003b5b2c: 0f28c6           movaps xmm0, xmm6
lodc 003b5b2f: f30f59c3         mulss xmm0, xmm3
lodc 003b5b33: f30f58c1         addss xmm0, xmm1
lodc 003b5b37: f30f110d6d36f201 movss dword ptr [rip + 0x1f2366d], xmm1
lodc 003b5b3f: f30f11058536f201 movss dword ptr [rip + 0x1f23685], xmm0
lodc 003b5b47: 0f5ac0           cvtps2pd xmm0, xmm0
lodc 003b5b4a: 0f54052f629301   andps xmm0, xmmword ptr [rip + 0x193622f]
lodc 003b5b51: 660f5ac0         cvtpd2ps xmm0, xmm0
lodc 003b5b55: e8bac34a00       call 0x861f14
lodc 003b5b5a: f30f101d8e38b401 movss xmm3, dword ptr [rip + 0x1b4388e]
lodc 003b5b62: 0f28e6           movaps xmm4, xmm6
lodc 003b5b65: f30f10156736f201 movss xmm2, dword ptr [rip + 0x1f23667]
lodc 003b5b6d: f30f58e3         addss xmm4, xmm3
lodc 003b5b71: 488b7c2458       mov rdi, qword ptr [rsp + 0x58]
lodc 003b5b76: 0f28cb           movaps xmm1, xmm3
lodc 003b5b79: f30f58c8         addss xmm1, xmm0
lodc 003b5b7d: f30f11051336f201 movss dword ptr [rip + 0x1f23613], xmm0
lodc 003b5b85: f30f11256336f201 movss dword ptr [rip + 0x1f23663], xmm4
lodc 003b5b8d: f30f5f0d3b36f201 maxss xmm1, dword ptr [rip + 0x1f2363b]
lodc 003b5b95: f30f5dd1         minss xmm2, xmm1
lodc 003b5b99: f30f5c152f36f201 subss xmm2, dword ptr [rip + 0x1f2362f]
lodc 003b5ba1: f30f59153336f201 mulss xmm2, dword ptr [rip + 0x1f23633]
lodc 003b5ba9: f30f5ce2         subss xmm4, xmm2
lodc 003b5bad: f30f5fe3         maxss xmm4, xmm3
lodc 003b5bb1: f30f5de6         minss xmm4, xmm6
lodc 003b5bb5: 0f28742430       movaps xmm6, xmmword ptr [rsp + 0x30]
lodc 003b5bba: f30f1125fe35f201 movss dword ptr [rip + 0x1f235fe], xmm4
lodc 003b5bc2: 0f1005f735f201   movups xmm0, xmmword ptr [rip + 0x1f235f7]
lodc 003b5bc9: 0f1105e033f201   movups xmmword ptr [rip + 0x1f233e0], xmm0
lodc 003b5bd0: 660f7e442450     movd dword ptr [rsp + 0x50], xmm0
lodc 003b5bd6: f30f10442450     movss xmm0, dword ptr [rsp + 0x50]
lodc 003b5bdc: 4883c440         add rsp, 0x40
lodc 003b5be0: 5b               pop rbx
lodc 003b5be1: c3               ret 
lodc 003b5be2: f30f1005be5f9301 movss xmm0, dword ptr [rip + 0x1935fbe]
lodc 003b5bea: 488b7c2458       mov rdi, qword ptr [rsp + 0x58]
lodc 003b5bef: 4883c440         add rsp, 0x40
lodc 003b5bf3: 5b               pop rbx
lodc 003b5bf4: c3               ret 
lodc 003b5bf5: cc               int3 
lodc 003b5bf6: cc               int3 
lodc 003b5bf7: cc               int3 
lodc 003b5bf8: cc               int3 
lodc 003b5bf9: cc               int3 
lodc 003b5bfa: cc               int3 
lodc 003b5bfb: cc               int3 
lodc 003b5bfc: cc               int3 
lodc 003b5bfd: cc               int3 
lodc 003b5bfe: cc               int3 
lodc 003b5bff: cc               int3 
lodc 003b5c00: 0fb6d1           movzx edx, cl
lodc 003b5c03: 4869c2e0000000   imul rax, rdx, 0xe0
lodc 003b5c0a: 48030517a97802   add rax, qword ptr [rip + 0x278a917]
lodc 003b5c11: 394810           cmp dword ptr [rax + 0x10], ecx
lodc 003b5c14: 0f85bb000000     jne 0x3b5cd5
lodc 003b5c1a: f6404001         test byte ptr [rax + 0x40], 1
lodc 003b5c1e: 0f84b1000000     je 0x3b5cd5
lodc 003b5c24: 0fb608           movzx ecx, byte ptr [rax]
lodc 003b5c27: 84c9             test cl, cl
lodc 003b5c29: 7422             je 0x3b5c4d
lodc 003b5c2b: f30f104060       movss xmm0, dword ptr [rax + 0x60]
lodc 003b5c30: fec9             dec cl
lodc 003b5c32: f30f104864       movss xmm1, dword ptr [rax + 0x64]
lodc 003b5c37: f30f584050       addss xmm0, dword ptr [rax + 0x50]
lodc 003b5c3c: f30f584854       addss xmm1, dword ptr [rax + 0x54]
lodc 003b5c41: 8808             mov byte ptr [rax], cl
lodc 003b5c43: f30f114050       movss dword ptr [rax + 0x50], xmm0
lodc 003b5c48: f30f114854       movss dword ptr [rax + 0x54], xmm1
lodc 003b5c4d: 0fb64802         movzx ecx, byte ptr [rax + 2]
lodc 003b5c51: 84c9             test cl, cl
lodc 003b5c53: 7423             je 0x3b5c78
lodc 003b5c55: f30f104068       movss xmm0, dword ptr [rax + 0x68]
lodc 003b5c5a: fec9             dec cl
lodc 003b5c5c: f30f10486c       movss xmm1, dword ptr [rax + 0x6c]
lodc 003b5c61: f30f584058       addss xmm0, dword ptr [rax + 0x58]
lodc 003b5c66: f30f58485c       addss xmm1, dword ptr [rax + 0x5c]
lodc 003b5c6b: 884802           mov byte ptr [rax + 2], cl
lodc 003b5c6e: f30f114058       movss dword ptr [rax + 0x58], xmm0
lodc 003b5c73: f30f11485c       movss dword ptr [rax + 0x5c], xmm1
lodc 003b5c78: 0fb64801         movzx ecx, byte ptr [rax + 1]
lodc 003b5c7c: 84c9             test cl, cl
lodc 003b5c7e: 7414             je 0x3b5c94
lodc 003b5c80: f30f104074       movss xmm0, dword ptr [rax + 0x74]
lodc 003b5c85: fec9             dec cl
lodc 003b5c87: f30f584070       addss xmm0, dword ptr [rax + 0x70]
lodc 003b5c8c: 884801           mov byte ptr [rax + 1], cl
lodc 003b5c8f: f30f114070       movss dword ptr [rax + 0x70], xmm0
lodc 003b5c94: 0fb64803         movzx ecx, byte ptr [rax + 3]
lodc 003b5c98: 84c9             test cl, cl
lodc 003b5c9a: 7414             je 0x3b5cb0
lodc 003b5c9c: f30f10407c       movss xmm0, dword ptr [rax + 0x7c]
lodc 003b5ca1: fec9             dec cl
lodc 003b5ca3: f30f584078       addss xmm0, dword ptr [rax + 0x78]
lodc 003b5ca8: 884803           mov byte ptr [rax + 3], cl
lodc 003b5cab: f30f114078       movss dword ptr [rax + 0x78], xmm0
lodc 003b5cb0: 0fb64843         movzx ecx, byte ptr [rax + 0x43]
lodc 003b5cb4: 84c9             test cl, cl
lodc 003b5cb6: 741d             je 0x3b5cd5
lodc 003b5cb8: f30f10809c000000 movss xmm0, dword ptr [rax + 0x9c]
lodc 003b5cc0: fec9             dec cl
lodc 003b5cc2: f30f588098000000 addss xmm0, dword ptr [rax + 0x98]
lodc 003b5cca: 884843           mov byte ptr [rax + 0x43], cl
lodc 003b5ccd: f30f118098000000 movss dword ptr [rax + 0x98], xmm0
lodc 003b5cd5: c3               ret 
lodc 003b5cd6: cc               int3 
lodc 003b5cd7: cc               int3 
lodc 003b5cd8: cc               int3 
lodc 003b5cd9: cc               int3 
lodc 003b5cda: cc               int3 
lodc 003b5cdb: cc               int3 
lodc 003b5cdc: cc               int3 
lodc 003b5cdd: cc               int3 
lodc 003b5cde: cc               int3 
lodc 003b5cdf: cc               int3 
lodc 003b5ce0: 440fb6c1         movzx r8d, cl
lodc 003b5ce4: 4d69c8e0000000   imul r9, r8, 0xe0
lodc 003b5ceb: 4c030d36a87802   add r9, qword ptr [rip + 0x278a836]
lodc 003b5cf2: 41394910         cmp dword ptr [r9 + 0x10], ecx
lodc 003b5cf6: 753f             jne 0x3b5d37
lodc 003b5cf8: 418b4148         mov eax, dword ptr [r9 + 0x48]
lodc 003b5cfc: 41894130         mov dword ptr [r9 + 0x30], eax
lodc 003b5d00: 418b414c         mov eax, dword ptr [r9 + 0x4c]
lodc 003b5d04: 41894134         mov dword ptr [r9 + 0x34], eax
lodc 003b5d08: 410fb74138       movzx eax, word ptr [r9 + 0x38]
lodc 003b5d0d: 664189413a       mov word ptr [r9 + 0x3a], ax
lodc 003b5d12: f3410f115148     movss dword ptr [r9 + 0x48], xmm2
lodc 003b5d18: f3410f11594c     movss dword ptr [r9 + 0x4c], xmm3
lodc 003b5d1e: 85d2             test edx, edx
lodc 003b5d20: 750b             jne 0x3b5d2d
lodc 003b5d22: 410fb7413c       movzx eax, word ptr [r9 + 0x3c]
lodc 003b5d27: 6641894138       mov word ptr [r9 + 0x38], ax
lodc 003b5d2c: c3               ret 
lodc 003b5d2d: 410fb7413e       movzx eax, word ptr [r9 + 0x3e]
lodc 003b5d32: 6641894138       mov word ptr [r9 + 0x38], ax
lodc 003b5d37: c3               ret 
lodc 003b5d38: cc               int3 
lodc 003b5d39: cc               int3 
lodc 003b5d3a: cc               int3 
lodc 003b5d3b: cc               int3 
lodc 003b5d3c: cc               int3 
lodc 003b5d3d: cc               int3 
lodc 003b5d3e: cc               int3 
lodc 003b5d3f: cc               int3 
lodc 003b5d40: 440fb6c1         movzx r8d, cl
lodc 003b5d44: 4d69c8e0000000   imul r9, r8, 0xe0
lodc 003b5d4b: 4c030dd6a77802   add r9, qword ptr [rip + 0x278a7d6]
lodc 003b5d52: 41394910         cmp dword ptr [r9 + 0x10], ecx
lodc 003b5d56: 0f85b8000000     jne 0x3b5e14
lodc 003b5d5c: 418b81c0000000   mov eax, dword ptr [r9 + 0xc0]
lodc 003b5d63: 41898180000000   mov dword ptr [r9 + 0x80], eax
lodc 003b5d6a: 418b81c4000000   mov eax, dword ptr [r9 + 0xc4]
lodc 003b5d71: 41898184000000   mov dword ptr [r9 + 0x84], eax
lodc 003b5d78: 418b81c8000000   mov eax, dword ptr [r9 + 0xc8]
lodc 003b5d7f: 41898188000000   mov dword ptr [r9 + 0x88], eax
lodc 003b5d86: 418b81cc000000   mov eax, dword ptr [r9 + 0xcc]
lodc 003b5d8d: 4189818c000000   mov dword ptr [r9 + 0x8c], eax
lodc 003b5d94: 418b81d0000000   mov eax, dword ptr [r9 + 0xd0]
lodc 003b5d9b: 41898190000000   mov dword ptr [r9 + 0x90], eax
lodc 003b5da2: 418b81d4000000   mov eax, dword ptr [r9 + 0xd4]
lodc 003b5da9: 41898194000000   mov dword ptr [r9 + 0x94], eax
lodc 003b5db0: 41885143         mov byte ptr [r9 + 0x43], dl
lodc 003b5db4: 41c7819800000000000000 mov dword ptr [r9 + 0x98], 0
lodc 003b5dbf: c7058333f2010000803f mov dword ptr [rip + 0x1f23383], 0x3f800000
lodc 003b5dc9: f30f10057b33f201 movss xmm0, dword ptr [rip + 0x1f2337b]
lodc 003b5dd1: 89157133f201     mov dword ptr [rip + 0x1f23371], edx
lodc 003b5dd7: f30f5e056933f201 divss xmm0, dword ptr [rip + 0x1f23369]
lodc 003b5ddf: 48c705a631f2010000803f mov qword ptr [rip + 0x1f231a6], 0x3f800000
lodc 003b5dea: 410fb64143       movzx eax, byte ptr [r9 + 0x43]
lodc 003b5def: f3410f11819c000000 movss dword ptr [r9 + 0x9c], xmm0
lodc 003b5df8: 84c0             test al, al
lodc 003b5dfa: 7418             je 0x3b5e14
lodc 003b5dfc: f3410f588198000000 addss xmm0, dword ptr [r9 + 0x98]
lodc 003b5e05: fec8             dec al
lodc 003b5e07: 41884143         mov byte ptr [r9 + 0x43], al
lodc 003b5e0b: f3410f118198000000 movss dword ptr [r9 + 0x98], xmm0
lodc 003b5e14: c3               ret 
lodc 003b5e15: cc               int3 
lodc 003b5e16: cc               int3 
lodc 003b5e17: cc               int3 
lodc 003b5e18: cc               int3 
lodc 003b5e19: cc               int3 
lodc 003b5e1a: cc               int3 
lodc 003b5e1b: cc               int3 
lodc 003b5e1c: cc               int3 
lodc 003b5e1d: cc               int3 
lodc 003b5e1e: cc               int3 
lodc 003b5e1f: cc               int3 
lodc 003b5e20: 440fb6c1         movzx r8d, cl
lodc 003b5e24: 4c8bd2           mov r10, rdx
lodc 003b5e27: 4d69c8e0000000   imul r9, r8, 0xe0
lodc 003b5e2e: 4c030df3a67802   add r9, qword ptr [rip + 0x278a6f3]
lodc 003b5e35: 41394910         cmp dword ptr [r9 + 0x10], ecx
lodc 003b5e39: 0f85b9010000     jne 0x3b5ff8
lodc 003b5e3f: 410fb64940       movzx ecx, byte ptr [r9 + 0x40]
lodc 003b5e44: f6c102           test cl, 2
lodc 003b5e47: 7434             je 0x3b5e7d
lodc 003b5e49: f3410f1089a0000000 movss xmm1, dword ptr [r9 + 0xa0]
lodc 003b5e52: f3410f1081a4000000 movss xmm0, dword ptr [r9 + 0xa4]
lodc 003b5e5b: f3410f114950     movss dword ptr [r9 + 0x50], xmm1
lodc 003b5e61: f3410f114154     movss dword ptr [r9 + 0x54], xmm0
lodc 003b5e67: f3410f118980000000 movss dword ptr [r9 + 0x80], xmm1
lodc 003b5e70: f3410f118184000000 movss dword ptr [r9 + 0x84], xmm0
lodc 003b5e79: 41c60100         mov byte ptr [r9], 0
lodc 003b5e7d: f6c104           test cl, 4
lodc 003b5e80: 741d             je 0x3b5e9f
lodc 003b5e82: f3410f1081b0000000 movss xmm0, dword ptr [r9 + 0xb0]
lodc 003b5e8b: f3410f114170     movss dword ptr [r9 + 0x70], xmm0
lodc 003b5e91: f3410f118190000000 movss dword ptr [r9 + 0x90], xmm0
lodc 003b5e9a: 41c6410300       mov byte ptr [r9 + 3], 0
lodc 003b5e9f: f6c108           test cl, 8
lodc 003b5ea2: 7435             je 0x3b5ed9
lodc 003b5ea4: f3410f1089a8000000 movss xmm1, dword ptr [r9 + 0xa8]
lodc 003b5ead: f3410f1081ac000000 movss xmm0, dword ptr [r9 + 0xac]
lodc 003b5eb6: f3410f114958     movss dword ptr [r9 + 0x58], xmm1
lodc 003b5ebc: f3410f11415c     movss dword ptr [r9 + 0x5c], xmm0
lodc 003b5ec2: f3410f118988000000 movss dword ptr [r9 + 0x88], xmm1
lodc 003b5ecb: f3410f11818c000000 movss dword ptr [r9 + 0x8c], xmm0
lodc 003b5ed4: 41c6410200       mov byte ptr [r9 + 2], 0
lodc 003b5ed9: f6c110           test cl, 0x10
lodc 003b5edc: 7416             je 0x3b5ef4
lodc 003b5ede: 418b81b4000000   mov eax, dword ptr [r9 + 0xb4]
lodc 003b5ee5: 41894148         mov dword ptr [r9 + 0x48], eax
lodc 003b5ee9: 418b81b8000000   mov eax, dword ptr [r9 + 0xb8]
lodc 003b5ef0: 4189414c         mov dword ptr [r9 + 0x4c], eax
lodc 003b5ef4: 66837a3200       cmp word ptr [rdx + 0x32], 0
lodc 003b5ef9: 745d             je 0x3b5f58
lodc 003b5efb: 8b424c           mov eax, dword ptr [rdx + 0x4c]
lodc 003b5efe: 418981a0000000   mov dword ptr [r9 + 0xa0], eax
lodc 003b5f05: 8b4250           mov eax, dword ptr [rdx + 0x50]
lodc 003b5f08: 418981a4000000   mov dword ptr [r9 + 0xa4], eax
lodc 003b5f0f: 0fb74232         movzx eax, word ptr [rdx + 0x32]
lodc 003b5f13: 66c1f806         sar ax, 6
lodc 003b5f17: 98               cwde 
lodc 003b5f18: 660f6ec0         movd xmm0, eax
lodc 003b5f1c: 0f5bc0           cvtdq2ps xmm0, xmm0
lodc 003b5f1f: f30f590589b69500 mulss xmm0, dword ptr [rip + 0x95b689]
lodc 003b5f27: f3410f1181b0000000 movss dword ptr [r9 + 0xb0], xmm0
lodc 003b5f30: 8b4258           mov eax, dword ptr [rdx + 0x58]
lodc 003b5f33: 418981b4000000   mov dword ptr [r9 + 0xb4], eax
lodc 003b5f3a: 8b425c           mov eax, dword ptr [rdx + 0x5c]
lodc 003b5f3d: 418981b8000000   mov dword ptr [r9 + 0xb8], eax
lodc 003b5f44: 8b4210           mov eax, dword ptr [rdx + 0x10]
lodc 003b5f47: 418981a8000000   mov dword ptr [r9 + 0xa8], eax
lodc 003b5f4e: 8b4254           mov eax, dword ptr [rdx + 0x54]
lodc 003b5f51: 418981ac000000   mov dword ptr [r9 + 0xac], eax
lodc 003b5f58: 0fb74232         movzx eax, word ptr [rdx + 0x32]
lodc 003b5f5c: 66c1e00f         shl ax, 0xf
lodc 003b5f60: 66c1f80f         sar ax, 0xf
lodc 003b5f64: 02c0             add al, al
lodc 003b5f66: 32c1             xor al, cl
lodc 003b5f68: 2402             and al, 2
lodc 003b5f6a: 32c1             xor al, cl
lodc 003b5f6c: 41884140         mov byte ptr [r9 + 0x40], al
lodc 003b5f70: 0fb74a32         movzx ecx, word ptr [rdx + 0x32]
lodc 003b5f74: 66c1e10e         shl cx, 0xe
lodc 003b5f78: 66c1f90f         sar cx, 0xf
lodc 003b5f7c: c0e102           shl cl, 2
lodc 003b5f7f: 32c8             xor cl, al
lodc 003b5f81: 80e104           and cl, 4
lodc 003b5f84: 32c8             xor cl, al
lodc 003b5f86: 41884940         mov byte ptr [r9 + 0x40], cl
lodc 003b5f8a: 0fb74232         movzx eax, word ptr [rdx + 0x32]
lodc 003b5f8e: 66c1e00c         shl ax, 0xc
lodc 003b5f92: 66c1f80f         sar ax, 0xf
lodc 003b5f96: c0e003           shl al, 3
lodc 003b5f99: 32c1             xor al, cl
lodc 003b5f9b: 2408             and al, 8
lodc 003b5f9d: 32c1             xor al, cl
lodc 003b5f9f: 41884140         mov byte ptr [r9 + 0x40], al
lodc 003b5fa3: 0fb74a32         movzx ecx, word ptr [rdx + 0x32]
lodc 003b5fa7: 66c1e10d         shl cx, 0xd
lodc 003b5fab: 66c1f90f         sar cx, 0xf
lodc 003b5faf: c0e104           shl cl, 4
lodc 003b5fb2: 32c8             xor cl, al
lodc 003b5fb4: 80e110           and cl, 0x10
lodc 003b5fb7: 32c8             xor cl, al
lodc 003b5fb9: 41884940         mov byte ptr [r9 + 0x40], cl
lodc 003b5fbd: 0fb75232         movzx edx, word ptr [rdx + 0x32]
lodc 003b5fc1: 66c1e20b         shl dx, 0xb
lodc 003b5fc5: 66c1fa0f         sar dx, 0xf
lodc 003b5fc9: c0e205           shl dl, 5
lodc 003b5fcc: 32d1             xor dl, cl
lodc 003b5fce: 80e220           and dl, 0x20
lodc 003b5fd1: 32d1             xor dl, cl
lodc 003b5fd3: 41885140         mov byte ptr [r9 + 0x40], dl
lodc 003b5fd7: 410fb74232       movzx eax, word ptr [r10 + 0x32]
lodc 003b5fdc: 66c1e00a         shl ax, 0xa
lodc 003b5fe0: 66c1f80f         sar ax, 0xf
lodc 003b5fe4: c0e006           shl al, 6
lodc 003b5fe7: 32c2             xor al, dl
lodc 003b5fe9: 41c70100000000   mov dword ptr [r9], 0
lodc 003b5ff0: 2440             and al, 0x40
lodc 003b5ff2: 32c2             xor al, dl
lodc 003b5ff4: 41884140         mov byte ptr [r9 + 0x40], al
lodc 003b5ff8: c3               ret 
lodc 003b5ff9: cc               int3 
lodc 003b5ffa: cc               int3 
lodc 003b5ffb: cc               int3 
lodc 003b5ffc: cc               int3 
lodc 003b5ffd: cc               int3 
lodc 003b5ffe: cc               int3 
lodc 003b5fff: cc               int3 
lodc 003b6000: 0fb6d1           movzx edx, cl
lodc 003b6003: 4869c2e0000000   imul rax, rdx, 0xe0
lodc 003b600a: 48030517a57802   add rax, qword ptr [rip + 0x278a517]
lodc 003b6011: 394810           cmp dword ptr [rax + 0x10], ecx
lodc 003b6014: 7504             jne 0x3b601a
lodc 003b6016: 806040fe         and byte ptr [rax + 0x40], 0xfe
lodc 003b601a: c3               ret 
lodc 003b601b: cc               int3 
lodc 003b601c: cc               int3 
lodc 003b601d: cc               int3 
lodc 003b601e: cc               int3 
lodc 003b601f: cc               int3 
leaf 0036dd80: 0f280549825500   movaps xmm0, xmmword ptr [rip + 0x558249]
leaf 0036dd87: 0f110562b6b801   movups xmmword ptr [rip + 0x1b8b662], xmm0
leaf 0036dd8e: c3               ret 