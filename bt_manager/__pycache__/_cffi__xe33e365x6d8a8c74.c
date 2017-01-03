
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
   typedef unsigned char _Bool;
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    ((type)(                                                             \
     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0)))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    (void)self; /* unused */
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/


#include "rtpsbc.h"

static int _cffi_e_____D_enum____D_1(PyObject *lib)
{
  if ((SBC_FREQ_16000) > 0 || (long)(SBC_FREQ_16000) != 0L) {
    char buf[64];
    if ((SBC_FREQ_16000) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_FREQ_16000));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_FREQ_16000));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$1: ", "SBC_FREQ_16000", buf, "0");
    return -1;
  }
  if ((SBC_FREQ_32000) <= 0 || (unsigned long)(SBC_FREQ_32000) != 1UL) {
    char buf[64];
    if ((SBC_FREQ_32000) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_FREQ_32000));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_FREQ_32000));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$1: ", "SBC_FREQ_32000", buf, "1");
    return -1;
  }
  if ((SBC_FREQ_44100) <= 0 || (unsigned long)(SBC_FREQ_44100) != 2UL) {
    char buf[64];
    if ((SBC_FREQ_44100) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_FREQ_44100));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_FREQ_44100));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$1: ", "SBC_FREQ_44100", buf, "2");
    return -1;
  }
  if ((SBC_FREQ_48000) <= 0 || (unsigned long)(SBC_FREQ_48000) != 3UL) {
    char buf[64];
    if ((SBC_FREQ_48000) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_FREQ_48000));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_FREQ_48000));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$1: ", "SBC_FREQ_48000", buf, "3");
    return -1;
  }
  return ((void)lib,0);
}

static int _cffi_e_____D_enum____D_2(PyObject *lib)
{
  if ((SBC_BLK_4) > 0 || (long)(SBC_BLK_4) != 0L) {
    char buf[64];
    if ((SBC_BLK_4) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_BLK_4));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_BLK_4));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$2: ", "SBC_BLK_4", buf, "0");
    return -1;
  }
  if ((SBC_BLK_8) <= 0 || (unsigned long)(SBC_BLK_8) != 1UL) {
    char buf[64];
    if ((SBC_BLK_8) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_BLK_8));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_BLK_8));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$2: ", "SBC_BLK_8", buf, "1");
    return -1;
  }
  if ((SBC_BLK_12) <= 0 || (unsigned long)(SBC_BLK_12) != 2UL) {
    char buf[64];
    if ((SBC_BLK_12) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_BLK_12));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_BLK_12));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$2: ", "SBC_BLK_12", buf, "2");
    return -1;
  }
  if ((SBC_BLK_16) <= 0 || (unsigned long)(SBC_BLK_16) != 3UL) {
    char buf[64];
    if ((SBC_BLK_16) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_BLK_16));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_BLK_16));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$2: ", "SBC_BLK_16", buf, "3");
    return -1;
  }
  return _cffi_e_____D_enum____D_1(lib);
}

static int _cffi_e_____D_enum____D_3(PyObject *lib)
{
  if ((SBC_MODE_MONO) > 0 || (long)(SBC_MODE_MONO) != 0L) {
    char buf[64];
    if ((SBC_MODE_MONO) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_MODE_MONO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_MODE_MONO));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$3: ", "SBC_MODE_MONO", buf, "0");
    return -1;
  }
  if ((SBC_MODE_DUAL_CHANNEL) <= 0 || (unsigned long)(SBC_MODE_DUAL_CHANNEL) != 1UL) {
    char buf[64];
    if ((SBC_MODE_DUAL_CHANNEL) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_MODE_DUAL_CHANNEL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_MODE_DUAL_CHANNEL));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$3: ", "SBC_MODE_DUAL_CHANNEL", buf, "1");
    return -1;
  }
  if ((SBC_MODE_STEREO) <= 0 || (unsigned long)(SBC_MODE_STEREO) != 2UL) {
    char buf[64];
    if ((SBC_MODE_STEREO) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_MODE_STEREO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_MODE_STEREO));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$3: ", "SBC_MODE_STEREO", buf, "2");
    return -1;
  }
  if ((SBC_MODE_JOINT_STEREO) <= 0 || (unsigned long)(SBC_MODE_JOINT_STEREO) != 3UL) {
    char buf[64];
    if ((SBC_MODE_JOINT_STEREO) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_MODE_JOINT_STEREO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_MODE_JOINT_STEREO));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$3: ", "SBC_MODE_JOINT_STEREO", buf, "3");
    return -1;
  }
  return _cffi_e_____D_enum____D_2(lib);
}

static int _cffi_e_____D_enum____D_4(PyObject *lib)
{
  if ((SBC_AM_LOUDNESS) > 0 || (long)(SBC_AM_LOUDNESS) != 0L) {
    char buf[64];
    if ((SBC_AM_LOUDNESS) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_AM_LOUDNESS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_AM_LOUDNESS));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$4: ", "SBC_AM_LOUDNESS", buf, "0");
    return -1;
  }
  if ((SBC_AM_SNR) <= 0 || (unsigned long)(SBC_AM_SNR) != 1UL) {
    char buf[64];
    if ((SBC_AM_SNR) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_AM_SNR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_AM_SNR));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$4: ", "SBC_AM_SNR", buf, "1");
    return -1;
  }
  return _cffi_e_____D_enum____D_3(lib);
}

static int _cffi_e_____D_enum____D_5(PyObject *lib)
{
  if ((SBC_SB_4) > 0 || (long)(SBC_SB_4) != 0L) {
    char buf[64];
    if ((SBC_SB_4) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_SB_4));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_SB_4));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$5: ", "SBC_SB_4", buf, "0");
    return -1;
  }
  if ((SBC_SB_8) <= 0 || (unsigned long)(SBC_SB_8) != 1UL) {
    char buf[64];
    if ((SBC_SB_8) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_SB_8));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_SB_8));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$5: ", "SBC_SB_8", buf, "1");
    return -1;
  }
  return _cffi_e_____D_enum____D_4(lib);
}

static int _cffi_e_____D_enum____D_6(PyObject *lib)
{
  if ((SBC_LE) > 0 || (long)(SBC_LE) != 0L) {
    char buf[64];
    if ((SBC_LE) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_LE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_LE));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$6: ", "SBC_LE", buf, "0");
    return -1;
  }
  if ((SBC_BE) <= 0 || (unsigned long)(SBC_BE) != 1UL) {
    char buf[64];
    if ((SBC_BE) <= 0)
        snprintf(buf, 63, "%ld", (long)(SBC_BE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(SBC_BE));
    PyErr_Format(_cffi_VerificationError,
                 "%s%s has the real value %s, not %s",
                 "enum $enum_$6: ", "SBC_BE", buf, "1");
    return -1;
  }
  return _cffi_e_____D_enum____D_5(lib);
}

static PyObject *
_cffi_f_rtp_sbc_decode_from_fd(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  char * x1;
  size_t x2;
  size_t x3;
  int x4;
  Py_ssize_t datasize;
  size_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:rtp_sbc_decode_from_fd", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(1), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, size_t);
  if (x3 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, int);
  if (x4 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = rtp_sbc_decode_from_fd(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, size_t);
}

static PyObject *
_cffi_f_rtp_sbc_encode_to_fd(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  char * x1;
  size_t x2;
  size_t x3;
  unsigned int * x4;
  unsigned int * x5;
  int x6;
  Py_ssize_t datasize;
  size_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;
  PyObject *arg6;

  if (!PyArg_ParseTuple(args, "OOOOOOO:rtp_sbc_encode_to_fd", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5, &arg6))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(1), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, size_t);
  if (x3 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca((size_t)datasize);
    memset((void *)x4, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(2), arg4) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca((size_t)datasize);
    memset((void *)x5, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(2), arg5) < 0)
      return NULL;
  }

  x6 = _cffi_to_c_int(arg6, int);
  if (x6 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = rtp_sbc_encode_to_fd(x0, x1, x2, x3, x4, x5, x6); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, size_t);
}

static PyObject *
_cffi_f_sbc_decode(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  void const * x1;
  size_t x2;
  void * x3;
  size_t x4;
  size_t * x5;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:sbc_decode", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(3), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(4), arg3) < 0)
      return NULL;
  }

  x4 = _cffi_to_c_int(arg4, size_t);
  if (x4 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca((size_t)datasize);
    memset((void *)x5, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(5), arg5) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_decode(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_sbc_encode(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  void const * x1;
  size_t x2;
  void * x3;
  size_t x4;
  ssize_t * x5;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:sbc_encode", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(3), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca((size_t)datasize);
    memset((void *)x3, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(4), arg3) < 0)
      return NULL;
  }

  x4 = _cffi_to_c_int(arg4, size_t);
  if (x4 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca((size_t)datasize);
    memset((void *)x5, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(6), arg5) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_encode(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_sbc_finish(PyObject *self, PyObject *arg0)
{
  sbc_t * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { sbc_finish(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_sbc_get_codesize(PyObject *self, PyObject *arg0)
{
  sbc_t * x0;
  Py_ssize_t datasize;
  size_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_get_codesize(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, size_t);
}

static PyObject *
_cffi_f_sbc_get_frame_duration(PyObject *self, PyObject *arg0)
{
  sbc_t * x0;
  Py_ssize_t datasize;
  unsigned int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_get_frame_duration(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, unsigned int);
}

static PyObject *
_cffi_f_sbc_get_frame_length(PyObject *self, PyObject *arg0)
{
  sbc_t * x0;
  Py_ssize_t datasize;
  size_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_get_frame_length(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, size_t);
}

static PyObject *
_cffi_f_sbc_get_implementation_info(PyObject *self, PyObject *arg0)
{
  sbc_t * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_get_implementation_info(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(8));
}

static PyObject *
_cffi_f_sbc_init(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  unsigned long x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:sbc_init", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned long);
  if (x1 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_init(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_sbc_parse(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  void const * x1;
  size_t x2;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:sbc_parse", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(3), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_parse(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_sbc_reinit(PyObject *self, PyObject *args)
{
  sbc_t * x0;
  unsigned long x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:sbc_reinit", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned long);
  if (x1 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = sbc_reinit(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static void _cffi_check_struct_sbc_struct(struct sbc_struct *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->flags) << 1);
  (void)((p->frequency) << 1);
  (void)((p->blocks) << 1);
  (void)((p->subbands) << 1);
  (void)((p->mode) << 1);
  (void)((p->allocation) << 1);
  (void)((p->bitpool) << 1);
  (void)((p->endian) << 1);
  { void * *tmp = &p->priv; (void)tmp; }
  { void * *tmp = &p->priv_alloc_base; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_sbc_struct(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct sbc_struct y; };
  static Py_ssize_t nums[] = {
    sizeof(struct sbc_struct),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct sbc_struct, flags),
    sizeof(((struct sbc_struct *)0)->flags),
    offsetof(struct sbc_struct, frequency),
    sizeof(((struct sbc_struct *)0)->frequency),
    offsetof(struct sbc_struct, blocks),
    sizeof(((struct sbc_struct *)0)->blocks),
    offsetof(struct sbc_struct, subbands),
    sizeof(((struct sbc_struct *)0)->subbands),
    offsetof(struct sbc_struct, mode),
    sizeof(((struct sbc_struct *)0)->mode),
    offsetof(struct sbc_struct, allocation),
    sizeof(((struct sbc_struct *)0)->allocation),
    offsetof(struct sbc_struct, bitpool),
    sizeof(((struct sbc_struct *)0)->bitpool),
    offsetof(struct sbc_struct, endian),
    sizeof(((struct sbc_struct *)0)->endian),
    offsetof(struct sbc_struct, priv),
    sizeof(((struct sbc_struct *)0)->priv),
    offsetof(struct sbc_struct, priv_alloc_base),
    sizeof(((struct sbc_struct *)0)->priv_alloc_base),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_sbc_struct(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_e_____D_enum____D_6(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"rtp_sbc_decode_from_fd", _cffi_f_rtp_sbc_decode_from_fd, METH_VARARGS, NULL},
  {"rtp_sbc_encode_to_fd", _cffi_f_rtp_sbc_encode_to_fd, METH_VARARGS, NULL},
  {"sbc_decode", _cffi_f_sbc_decode, METH_VARARGS, NULL},
  {"sbc_encode", _cffi_f_sbc_encode, METH_VARARGS, NULL},
  {"sbc_finish", _cffi_f_sbc_finish, METH_O, NULL},
  {"sbc_get_codesize", _cffi_f_sbc_get_codesize, METH_O, NULL},
  {"sbc_get_frame_duration", _cffi_f_sbc_get_frame_duration, METH_O, NULL},
  {"sbc_get_frame_length", _cffi_f_sbc_get_frame_length, METH_O, NULL},
  {"sbc_get_implementation_info", _cffi_f_sbc_get_implementation_info, METH_O, NULL},
  {"sbc_init", _cffi_f_sbc_init, METH_VARARGS, NULL},
  {"sbc_parse", _cffi_f_sbc_parse, METH_VARARGS, NULL},
  {"sbc_reinit", _cffi_f_sbc_reinit, METH_VARARGS, NULL},
  {"_cffi_layout_struct_sbc_struct", _cffi_layout_struct_sbc_struct, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__xe33e365x6d8a8c74",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__xe33e365x6d8a8c74(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (((void)lib,0) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__xe33e365x6d8a8c74(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__xe33e365x6d8a8c74", _cffi_methods);
  if (lib == NULL)
    return;
  if (((void)lib,0) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
