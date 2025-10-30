# Planka Performance Analysis: Slow Initial Website Loading

## Initial Load Process Analysis

The application follows this initialization sequence:

1. **Client-side startup**: React app loads via Vite
2. **Authentication check**: Determines if user is logged in
3. **Bootstrap fetch**: Calls `/api/bootstrap` endpoint
4. **Core data fetch**: Loads extensive application data (users, projects, boards, cards, etc.)
5. **UI rendering**: Displays content after all data is loaded

## Key Performance Issues

### 1. Heavy Initial Data Load
The `fetchCore()` function in `client/src/sagas/core/requests/core.js` performs multiple sequential API calls:
- `getCurrentUser` (with notifications)
- `getConfig` (for admins)
- `getWebhooks` (for admins)
- `getProjects` (with extensive includes)
- `fetchBoardByCurrentPath` (additional board/card data)
- `getNotifications`

This results in 5-8 API calls on initial load, many with large payloads.

### 2. Large Data Payloads
The `getProjects` endpoint includes extensive nested data:
- projectManagers, backgroundImages, baseCustomFieldGroups
- boards, users, boardMemberships, customFields, notificationServices

### 3. Synchronous Data Loading
All core data is loaded sequentially before the UI renders, showing a loading spinner until complete.

### 4. No Caching Strategy
Each page load fetches all data fresh, with no client-side caching of bootstrap or core data.

### 5. Heavy Frontend Bundle
The client has many dependencies (185 in package.json) and large CSS bundles, contributing to initial JavaScript load time.

## Implemented Optimizations ✅

### 1. Bootstrap Data Caching in localStorage
- **Status**: ✅ Implemented
- **Description**: Bootstrap data is now cached in localStorage with 5-minute expiration
- **Impact**: Eliminates `/api/bootstrap` network call on repeat visits
- **Files Modified**:
  - `client/src/utils/access-token-storage.js` - Added caching functions
  - `client/src/sagas/login/services/login.js` - Implemented caching logic
  - `client/src/sagas/core/services/core.js` - Clear cache on logout

### 2. Cache Management
- **Status**: ✅ Implemented
- **Description**: Bootstrap cache is automatically cleared on user logout
- **Impact**: Ensures data freshness while maintaining performance benefits

## Remaining Recommendations for Future Optimization

1. **Implement lazy loading** for non-critical data
2. **Add pagination** to large data sets (projects, users)
3. **Optimize bundle size** by code splitting
4. **Parallelize API calls** where possible (attempted but reverted due to stability issues)
5. **Add loading states** for different UI sections
6. **Implement service worker** for caching static assets

## Files Analyzed

- `client/src/sagas/core/requests/core.js` - Core data fetching logic
- `client/src/sagas/core/services/core.js` - Initialization orchestration
- `client/src/sagas/login/services/login.js` - Login bootstrap
- `server/api/controllers/bootstrap/show.js` - Bootstrap endpoint
- `client/src/components/common/Core/Core.jsx` - UI loading states
- `client/src/store.js` - Redux store setup
- `client/src/api/http.js` - HTTP client configuration
- `client/package.json` - Dependencies analysis

The main bottleneck appears to be the extensive data fetching required before any UI renders, combined with the lack of progressive loading strategies.
