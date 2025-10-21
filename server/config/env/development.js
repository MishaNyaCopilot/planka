const { URL } = require('url');

const origins = (process.env.BASE_URL || '').split(',').filter(Boolean).map((baseUrl) => new URL(baseUrl).origin);

module.exports = {
  security: {
    cors: {
      allRoutes: true,
      allowOrigins: origins,
      allowCredentials: true,
    },
  },
  sockets: {
    onlyAllowOrigins: origins,
  },
  http: {
    trustProxy: process.env.TRUST_PROXY === 'true',
  },
};
