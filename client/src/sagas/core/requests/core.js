/*!
 * Copyright (c) 2024 PLANKA Software GmbH
 * Licensed under the Fair Use License: https://github.com/plankanban/planka/blob/master/LICENSE.md
 */

import { call } from 'redux-saga/effects';

import { fetchBoardByCurrentPath } from './boards';
import request from '../request';
import api from '../../../api';
import mergeRecords from '../../../utils/merge-records';
import { isUserAdminOrProjectOwner } from '../../../utils/record-helpers';
import { UserRoles } from '../../../constants/Enums';

export function* fetchCore() {
  // Parallelize initial API calls
  const [userResponse, projectsResponse] = yield [
    call(request, api.getCurrentUser, true),
    call(request, api.getProjects),
  ];

  const {
    item: user,
    included: { notificationServices: notificationServices1 },
  } = userResponse;

  const {
    items: projects1,
    included: {
      projectManagers,
      backgroundImages,
      baseCustomFieldGroups,
      boards,
      users: users2,
      boardMemberships: boardMemberships1,
      customFields: customFields1,
      notificationServices: notificationServices2,
    },
  } = projectsResponse;

  // Parallelize admin-only calls
  let config;
  let webhooks;
  let users1;

  const adminCalls = [];
  if (user.role === UserRoles.ADMIN) {
    adminCalls.push(call(request, api.getConfig));
    adminCalls.push(call(request, api.getWebhooks));
  }

  if (isUserAdminOrProjectOwner(user)) {
    adminCalls.push(call(request, api.getUsers));
  }

  if (adminCalls.length > 0) {
    const adminResults = yield adminCalls;

    let resultIndex = 0;
    if (user.role === UserRoles.ADMIN) {
      ({ item: config } = adminResults[resultIndex++]);
      ({ items: webhooks } = adminResults[resultIndex++]);
    }

    if (isUserAdminOrProjectOwner(user)) {
      ({ items: users1 } = adminResults[resultIndex++]);
    }
  }

  let board;
  let card;
  let users3;
  let projects2;
  let boardMemberships2;
  let labels;
  let lists;
  let cards1;
  let cardMemberships;
  let cardLabels;
  let taskLists;
  let tasks;
  let attachments;
  let customFieldGroups;
  let customFields2;
  let customFieldValues;

  // Parallelize board data and notifications fetching
  const [boardData, notificationsBody] = yield [
    call(fetchBoardByCurrentPath),
    call(request, api.getNotifications),
  ].map(call => {
    try {
      return call;
    } catch {
      return null;
    }
  });

  if (boardData) {
    ({
      board,
      card,
      labels,
      lists,
      cardMemberships,
      cardLabels,
      taskLists,
      tasks,
      attachments,
      customFieldGroups,
      customFieldValues,
      users: users3,
      projects: projects2,
      boardMemberships: boardMemberships2,
      cards: cards1,
      customFields: customFields2,
    } = boardData);
  }

  const body = notificationsBody;

  let { items: notifications } = body;

  const {
    included: { users: users4 },
  } = body;

  if (card) {
    const notificationIds = notifications.flatMap((notification) =>
      notification.cardId === card.id ? notification.id : [],
    );

    if (notificationIds.length > 0) {
      yield call(request, api.readCardNotifications, card.id);

      notifications = notifications.filter(
        (notification) => !notificationIds.includes(notification.id),
      );
    }
  }

  return {
    config,
    user,
    board,
    webhooks,
    projectManagers,
    backgroundImages,
    baseCustomFieldGroups,
    boards,
    labels,
    lists,
    cardMemberships,
    cardLabels,
    taskLists,
    tasks,
    attachments,
    customFieldGroups,
    customFieldValues,
    notifications,
    users: mergeRecords(users1, users2, users3, users4),
    projects: mergeRecords(projects1, projects2),
    boardMemberships: mergeRecords(boardMemberships1, boardMemberships2),
    cards: mergeRecords(card && [card], cards1),
    customFields: mergeRecords(customFields1, customFields2),
    notificationServices: mergeRecords(notificationServices1, notificationServices2),
  };
}

export default {
  fetchCore,
};
