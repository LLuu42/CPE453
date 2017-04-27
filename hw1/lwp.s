	.file	"lwp.c"
	.globl	lwp_scheduler
	.bss
	.align 8
	.type	lwp_scheduler, @object
	.size	lwp_scheduler, 8
lwp_scheduler:
	.zero	8
	.comm	lwp_StackPointer,8,8
	.globl	nextPid
	.align 4
	.type	nextPid, @object
	.size	nextPid, 4
nextPid:
	.zero	4
	.comm	lwp_table,960,32
	.globl	lwp_procs
	.align 4
	.type	lwp_procs, @object
	.size	lwp_procs, 4
lwp_procs:
	.zero	4
	.comm	lwp_running,4,4
	.text
	.globl	new_lwp
	.type	new_lwp, @function
new_lwp:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	-72(%rbp), %rax
	salq	$2, %rax
	movq	%rax, -40(%rbp)
	movl	lwp_procs(%rip), %eax
	cmpl	$29, %eax
	jle	.L2
	movl	$-1, %eax
	jmp	.L3
.L2:
	movl	lwp_procs(%rip), %eax
	movl	%eax, lwp_running(%rip)
	movl	lwp_procs(%rip), %eax
	addl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movl	lwp_running(%rip), %eax
	movl	nextPid(%rip), %edx
	movl	%edx, %edx
	cltq
	salq	$5, %rax
	addq	$lwp_table, %rax
	movq	%rdx, (%rax)
	movl	nextPid(%rip), %eax
	addl	$1, %eax
	movl	%eax, nextPid(%rip)
	movl	lwp_running(%rip), %ebx
	movq	-40(%rbp), %rax
	movq	%rax, %rdi
	call	malloc
	movq	%rax, %rdx
	movslq	%ebx, %rax
	salq	$5, %rax
	addq	$lwp_table+8, %rax
	movq	%rdx, (%rax)
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	leaq	lwp_table+16(%rax), %rdx
	movq	-72(%rbp), %rax
	movq	%rax, (%rdx)
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table+8, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movq	%rax, -24(%rbp)
	movq	-64(%rbp), %rdx
	movq	-32(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -32(%rbp)
	movl	$lwp_exit, %edx
	movq	-32(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -32(%rbp)
	movq	-56(%rbp), %rdx
	movq	-32(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -32(%rbp)
	movq	-32(%rbp), %rax
	movl	$3735928559, %ecx
	movq	%rcx, (%rax)
	movq	-32(%rbp), %rax
	movq	%rax, -24(%rbp)
	subq	$56, -32(%rbp)
	movq	-24(%rbp), %rdx
	movq	-32(%rbp), %rax
	movq	%rdx, (%rax)
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	leaq	lwp_table+24(%rax), %rdx
	movq	-32(%rbp), %rax
	movq	%rax, (%rdx)
	movl	lwp_running(%rip), %eax
.L3:
	addq	$72, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	new_lwp, .-new_lwp
	.globl	lwp_exit
	.type	lwp_exit, @function
lwp_exit:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	$0, -4(%rbp)
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table+8, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	free
	movl	lwp_running(%rip), %eax
	addl	$1, %eax
	movl	%eax, -4(%rbp)
	jmp	.L5
.L6:
	movl	-4(%rbp), %eax
	subl	$1, %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table, %rax
	movl	-4(%rbp), %edx
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_table, %rdx
	movq	(%rdx), %rcx
	movq	%rcx, (%rax)
	movq	8(%rdx), %rcx
	movq	%rcx, 8(%rax)
	movq	16(%rdx), %rcx
	movq	%rcx, 16(%rax)
	movq	24(%rdx), %rdx
	movq	%rdx, 24(%rax)
	addl	$1, -4(%rbp)
.L5:
	movl	lwp_procs(%rip), %eax
	cmpl	%eax, -4(%rbp)
	jl	.L6
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	jne	.L7
	movl	$0, %eax
	call	lwp_stop
	jmp	.L11
.L7:
	movq	lwp_scheduler(%rip), %rax
	testq	%rax, %rax
	je	.L9
	movq	lwp_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, lwp_running(%rip)
	jmp	.L10
.L9:
	movl	$0, lwp_running(%rip)
.L10:
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table+24, %rax
	movq	(%rax), %rax
#APP
# 104 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 105 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 105 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 105 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
.L11:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	lwp_exit, .-lwp_exit
	.globl	lwp_getpid
	.type	lwp_getpid, @function
lwp_getpid:
.LFB4:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table, %rax
	movq	(%rax), %rax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	lwp_getpid, .-lwp_getpid
	.globl	lwp_yield
	.type	lwp_yield, @function
lwp_yield:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 126 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 126 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 126 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 126 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 126 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 126 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 126 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 126 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movl	lwp_running(%rip), %edx
#APP
# 128 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_table+24, %rdx
	movq	%rax, (%rdx)
	movq	lwp_scheduler(%rip), %rax
	testq	%rax, %rax
	je	.L15
	movq	lwp_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, lwp_running(%rip)
	jmp	.L16
.L15:
	movl	lwp_running(%rip), %eax
	addl	$1, %eax
	movl	%eax, lwp_running(%rip)
	movl	lwp_running(%rip), %edx
	movl	lwp_procs(%rip), %eax
	cmpl	%eax, %edx
	jl	.L16
	movl	$0, lwp_running(%rip)
.L16:
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table+24, %rax
	movq	(%rax), %rax
#APP
# 144 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 145 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 145 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 145 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	lwp_yield, .-lwp_yield
	.globl	lwp_start
	.type	lwp_start, @function
lwp_start:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	je	.L22
#APP
# 160 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 160 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 160 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 160 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 160 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 160 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 160 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 160 "lwp.c" 1
	pushq %rbp
# 0 "" 2
# 161 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movq	%rax, lwp_StackPointer(%rip)
	movq	lwp_scheduler(%rip), %rax
	testq	%rax, %rax
	je	.L20
	movq	lwp_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, lwp_running(%rip)
	jmp	.L21
.L20:
	movl	$0, lwp_running(%rip)
.L21:
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_table+24, %rax
	movq	(%rax), %rax
#APP
# 171 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 172 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 172 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 172 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	jmp	.L17
.L22:
	nop
.L17:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	lwp_start, .-lwp_start
	.globl	lwp_stop
	.type	lwp_stop, @function
lwp_stop:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 181 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 181 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 181 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 181 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 181 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 181 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 181 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 181 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movq	lwp_StackPointer(%rip), %rax
#APP
# 182 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 183 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 183 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 183 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	lwp_stop, .-lwp_stop
	.globl	lwp_set_scheduler
	.type	lwp_set_scheduler, @function
lwp_set_scheduler:
.LFB8:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, lwp_scheduler(%rip)
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	lwp_set_scheduler, .-lwp_set_scheduler
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
