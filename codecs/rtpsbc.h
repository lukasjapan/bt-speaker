enum {
SBC_FREQ_16000,
SBC_FREQ_32000,
SBC_FREQ_44100,
SBC_FREQ_48000,
};

enum {
SBC_BLK_4,
SBC_BLK_8,
SBC_BLK_12,
SBC_BLK_16
};

enum {
SBC_MODE_MONO,
SBC_MODE_DUAL_CHANNEL,
SBC_MODE_STEREO,
SBC_MODE_JOINT_STEREO
};

enum {
SBC_AM_LOUDNESS,
SBC_AM_SNR
};

enum {
SBC_SB_4,
SBC_SB_8
};

enum {
SBC_LE,
SBC_BE
};

struct sbc_struct {
	unsigned long flags;

	uint8_t frequency;
	uint8_t blocks;
	uint8_t subbands;
	uint8_t mode;
	uint8_t allocation;
	uint8_t bitpool;
	uint8_t endian;

	void *priv;
	void *priv_alloc_base;
};

typedef struct sbc_struct sbc_t;

int sbc_init(sbc_t *sbc, unsigned long flags);
int sbc_reinit(sbc_t *sbc, unsigned long flags);

ssize_t sbc_parse(sbc_t *sbc, const void *input, size_t input_len);

ssize_t sbc_decode(sbc_t *sbc, const void *input, size_t input_len,
			void *output, size_t output_len, size_t *written);

ssize_t sbc_encode(sbc_t *sbc, const void *input, size_t input_len,
			void *output, size_t output_len, ssize_t *written);

size_t sbc_get_frame_length(sbc_t *sbc);

unsigned sbc_get_frame_duration(sbc_t *sbc);

size_t sbc_get_codesize(sbc_t *sbc);

const char *sbc_get_implementation_info(sbc_t *sbc);
void sbc_finish(sbc_t *sbc);

size_t rtp_sbc_encode_to_fd(sbc_t *sbc, char *ip, size_t ip_size, size_t mtu,
                            unsigned int *ts, unsigned int *seq_num, int fd);
size_t rtp_sbc_decode_from_fd(sbc_t *sbc, char *op, size_t op_size, size_t mtu,
                              int fd);
