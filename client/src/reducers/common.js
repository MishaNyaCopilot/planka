/*!
 * Copyright (c) 2024 PLANKA Software GmbH
 * Licensed under the Fair Use License: https://github.com/plankanban/planka/blob/master/LICENSE.md
 */

import ActionTypes from '../constants/ActionTypes';

const initialState = {
  isInitializing: true,
  bootstrap: null,
  coreLoadingProgress: {
    user: false,
    projects: false,
    board: false,
    notifications: false,
  },
};

// eslint-disable-next-line default-param-last
export default (state = initialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SOCKET_RECONNECT_HANDLE:
      return {
        ...state,
        bootstrap: payload.bootstrap,
      };
    case ActionTypes.LOGIN_INITIALIZE:
      return {
        ...state,
        isInitializing: false,
        bootstrap: payload.bootstrap,
      };
    case ActionTypes.AUTHENTICATE__SUCCESS:
    case ActionTypes.WITH_OIDC_AUTHENTICATE__SUCCESS:
    case ActionTypes.TERMS_ACCEPT__SUCCESS:
      return {
        ...state,
        isInitializing: true,
      };
    case ActionTypes.CORE_INITIALIZE:
      return {
        ...state,
        isInitializing: false,
        coreLoadingProgress: {
          user: false,
          projects: false,
          board: false,
          notifications: false,
        },
      };
    case ActionTypes.CORE_LOADING_PROGRESS:
      return {
        ...state,
        coreLoadingProgress: {
          ...state.coreLoadingProgress,
          ...payload,
        },
      };
    case ActionTypes.CORE_INITIALIZE__BOOTSTRAP_FETCH:
      return {
        ...state,
        bootstrap: payload.bootstrap,
      };
    case ActionTypes.USER_UPDATE_HANDLE:
      if (payload.bootstrap) {
        return {
          ...state,
          bootstrap: payload.bootstrap,
        };
      }

      return state;
    default:
      return state;
  }
};
