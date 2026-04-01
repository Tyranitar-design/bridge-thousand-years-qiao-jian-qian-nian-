/**
 * 桥梁收藏功能 - 使用 localStorage 存储
 */

const FAVORITES_KEY = 'bridge_favorites'

/**
 * 获取所有收藏的桥梁ID列表
 */
export function getFavorites() {
  try {
    const data = localStorage.getItem(FAVORITES_KEY)
    return data ? JSON.parse(data) : []
  } catch (e) {
    console.error('读取收藏失败:', e)
    return []
  }
}

/**
 * 检查桥梁是否已收藏
 */
export function isFavorite(bridgeId) {
  const favorites = getFavorites()
  return favorites.includes(bridgeId)
}

/**
 * 添加收藏
 */
export function addFavorite(bridgeId) {
  const favorites = getFavorites()
  if (!favorites.includes(bridgeId)) {
    favorites.push(bridgeId)
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites))
    return true
  }
  return false
}

/**
 * 取消收藏
 */
export function removeFavorite(bridgeId) {
  let favorites = getFavorites()
  const index = favorites.indexOf(bridgeId)
  if (index > -1) {
    favorites.splice(index, 1)
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites))
    return true
  }
  return false
}

/**
 * 切换收藏状态
 * @returns {boolean} 收藏后的状态 (true=已收藏, false=未收藏)
 */
export function toggleFavorite(bridgeId) {
  if (isFavorite(bridgeId)) {
    removeFavorite(bridgeId)
    return false
  } else {
    addFavorite(bridgeId)
    return true
  }
}

/**
 * 获取收藏数量
 */
export function getFavoriteCount() {
  return getFavorites().length
}

/**
 * 清空所有收藏
 */
export function clearFavorites() {
  localStorage.removeItem(FAVORITES_KEY)
}
