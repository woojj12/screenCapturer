#include <linux/ptrace.h>
BPF_ARRAY(keyboardInputLog, unsigned, 2);
int on_keyboardInput(struct pt_regs *ctx, unsigned int keycode, int down,
                     bool hw_raw) {
  int updateFlagIdx = 0;
  int updateValueIdx = 1;
  unsigned bTrue = 1;

  keyboardInputLog.update(&updateFlagIdx, &bTrue);
  keyboardInputLog.update(&updateValueIdx, &keycode);

  return 0;
}
