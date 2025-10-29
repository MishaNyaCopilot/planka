/*!
 * Copyright (c) 2024 PLANKA Software GmbH
 * Licensed under the Fair Use License: https://github.com/plankanban/planka/blob/master/LICENSE.md
 */

import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

import Config from '../constants/Config';

export const setAccessToken = (accessToken) => {
  const { exp } = jwtDecode(accessToken);
  const expires = new Date(exp * 1000);

  Cookies.set(Config.ACCESS_TOKEN_KEY, accessToken, {
    expires,
    secure: window.location.protocol === 'https:',
    sameSite: 'strict',
  });

  Cookies.set(Config.ACCESS_TOKEN_VERSION_KEY, Config.ACCESS_TOKEN_VERSION, {
    expires,
  });
};

export const removeAccessToken = () => {
  Cookies.remove(Config.ACCESS_TOKEN_KEY);
  Cookies.remove(Config.ACCESS_TOKEN_VERSION_KEY);
};

export const getAccessToken = () => {
  let accessToken = Cookies.get(Config.ACCESS_TOKEN_KEY);
  const accessTokenVersion = Cookies.get(Config.ACCESS_TOKEN_VERSION_KEY);

  if (accessToken && accessTokenVersion !== Config.ACCESS_TOKEN_VERSION) {
    removeAccessToken();
    accessToken = undefined;
  }

  return accessToken;
};

export const setBootstrapCache = (bootstrap) => {
  try {
    localStorage.setItem('planka_bootstrap', JSON.stringify({
      data: bootstrap,
      timestamp: Date.now(),
    }));
  } catch (error) {
    // Silently fail if localStorage is not available
  }
};

export const getBootstrapCache = () => {
  try {
    const cached = localStorage.getItem('planka_bootstrap');
    if (!cached) return null;

    const { data, timestamp } = JSON.parse(cached);
    // Cache for 5 minutes
    if (Date.now() - timestamp > 5 * 60 * 1000) {
      localStorage.removeItem('planka_bootstrap');
      return null;
    }

    return data;
  } catch (error) {
    return null;
  }
};

export const clearBootstrapCache = () => {
  try {
    localStorage.removeItem('planka_bootstrap');
  } catch (error) {
    // Silently fail
  }
};
