const AccessTokenSteps = {
  ACCEPT_TERMS: 'accept-terms',
};

const POSITION_GAP = 65536;

const MAX_SIZE_TO_GET_ENCODING = 8 * 1024 * 1024;

// File upload security constants
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
const ALLOWED_MIME_TYPES = [
  // Images
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'image/svg+xml',
  // Documents
  'application/pdf',
  'text/plain',
  'text/markdown',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-powerpoint',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  // Archives
  'application/zip',
  'application/x-rar-compressed',
  'application/x-7z-compressed',
];

module.exports = {
  AccessTokenSteps,
  POSITION_GAP,
  MAX_SIZE_TO_GET_ENCODING,
  MAX_FILE_SIZE,
  ALLOWED_MIME_TYPES,
};
