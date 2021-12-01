#include <linux/ptrace.h>
#include <linux/libps2.h>

enum psmouse_state {
  PSMOUSE_IGNORE,
  PSMOUSE_INITIALIZING,
  PSMOUSE_RESYNCING,
  PSMOUSE_CMD_MODE,
  PSMOUSE_ACTIVATED,
};

/* psmouse protocol handler return codes */
typedef enum {
  PSMOUSE_BAD_DATA,
  PSMOUSE_GOOD_DATA,
  PSMOUSE_FULL_PACKET
} psmouse_ret_t;

enum psmouse_scale { PSMOUSE_SCALE11, PSMOUSE_SCALE21 };

struct psmouse {
  void *private;
  struct input_dev *dev;
  struct ps2dev ps2dev;
  struct delayed_work resync_work;
  const char *vendor;
  const char *name;
  const struct psmouse_protocol *protocol;
  unsigned char packet[8];
  unsigned char badbyte;
  unsigned char pktcnt;
  unsigned char pktsize;
  unsigned char oob_data_type;
  unsigned char extra_buttons;
  bool acks_disable_command;
  unsigned int model;
  unsigned long last;
  unsigned long out_of_sync_cnt;

  unsigned long num_resyncs;
  enum psmouse_state state;
  char devname[64];
  char phys[32];

  unsigned int rate;
  unsigned int resolution;
  unsigned int resetafter;
  unsigned int resync_time;
  bool smartscroll; /* Logitech only */

  psmouse_ret_t (*protocol_handler)(struct psmouse *psmouse);
  void (*set_rate)(struct psmouse *psmouse, unsigned int rate);
  void (*set_resolution)(struct psmouse *psmouse, unsigned int resolution);
  void (*set_scale)(struct psmouse *psmouse, enum psmouse_scale scale);

  int (*reconnect)(struct psmouse *psmouse);
  int (*fast_reconnect)(struct psmouse *psmouse);
  void (*disconnect)(struct psmouse *psmouse);
  void (*cleanup)(struct psmouse *psmouse);
  int (*poll)(struct psmouse *psmouse);

  void (*pt_activate)(struct psmouse *psmouse);
  void (*pt_deactivate)(struct psmouse *psmouse);
};

BPF_ARRAY(mouseClickLog, unsigned, 2);

int on_mouseClick(struct pt_regs *ctx, struct psmouse *psmouse) {
  unsigned mouseButton = (unsigned)psmouse->packet[0];

  int updateFlagIdx = 0;
  int updateValueIdx = 1;
  unsigned bTrue = 1;

  mouseClickLog.update(&updateFlagIdx, &bTrue);
  mouseClickLog.update(&updateValueIdx, &mouseButton);
  return 0;
}
