#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "sbc.h"
#include "rtp.h"


size_t rtp_sbc_encode_to_fd(sbc_t *sbc, char *ip, size_t ip_size, size_t mtu,
                            unsigned int *ts, unsigned int *seq_num, int fd)
{
    char buf[512];
    struct rtp_header *rtp_header = (struct rtp_header *)buf;
	struct rtp_payload *rtp_payload = (struct rtp_payload *)(buf + sizeof(*rtp_header));
    const size_t codesize = sbc_get_codesize(sbc);
    const size_t rtp_size = sizeof(*rtp_header) + sizeof(*rtp_payload);
    size_t index = 0;

    while (ip_size >= codesize) {

        char *op = &buf[rtp_size];
        size_t buf_size = mtu - rtp_size;
        size_t nbytes = rtp_size;
        size_t nframes = 0;

        memset(buf, 0, rtp_size);

        rtp_header->v = 2;
		rtp_header->pt = 1;
		rtp_header->sequence_number = *seq_num;
		rtp_header->timestamp = htonl(*ts);
		rtp_header->ssrc = htonl(1);

		while (ip_size >= codesize) {
			ssize_t encoded;
			ssize_t sz = sbc_encode(sbc,
									(void *)&ip[index],
									codesize,
									(void *)op,
									buf_size,
									&encoded);
			if (sz <= 0)
				break;

			ip_size -= sz;
			index += sz;
			buf_size -= encoded;
			nbytes += encoded;
			op += encoded;
			nframes++;
		}

		rtp_payload->frame_count = nframes;
		*ts += sbc_get_frame_duration(sbc) * nframes;
		(*seq_num)++;

		write(fd, buf, nbytes);
    }

    return index;
}


size_t rtp_sbc_decode_from_fd(sbc_t *sbc, char *op, size_t op_size, size_t mtu,
                              int fd)
{
    char buf[1024];
    struct rtp_header *rtp_header = (struct rtp_header *)buf;
	struct rtp_payload *rtp_payload = (struct rtp_payload *)(buf + sizeof(*rtp_header));
    const size_t codesize = sbc_get_codesize(sbc);
    const size_t frame_len = sbc_get_frame_length(sbc);
    const size_t rtp_size = sizeof(*rtp_header) + sizeof(*rtp_payload);
    const size_t mtu_round = ((mtu - rtp_size) / frame_len) * frame_len + rtp_size;
    size_t index = 0;

    while (op_size >= codesize) {

        char *ip = &buf[rtp_size];
        size_t nframes;
        ssize_t buf_size = read(fd, buf, mtu_round);

		if (buf_size <= 0)
        	break;

        nframes = rtp_payload->frame_count;
		buf_size -= rtp_size;

		while (buf_size > 0) {
			ssize_t decoded;
			ssize_t sz = sbc_decode(sbc,
									(void *)ip,
									buf_size,
									(void *)&op[index],
									op_size,
									&decoded);
			if (decoded <= 0)
				break;

			ip += sz;
			buf_size -= sz;
			index += decoded;
			op_size -= decoded;
		}
    }

    return index;
}
