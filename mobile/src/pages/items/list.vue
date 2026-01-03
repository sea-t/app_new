<template>
  <view class="container">
    <view class="header">
      <text class="title">待办清单</text>
      <button class="add-btn" type="primary" size="mini" @click="goToCreate">新增</button>
    </view>

    <view v-if="loading" class="loading">
      <text>加载中...</text>
    </view>

    <view v-else-if="items.length === 0" class="empty">
      <text>暂无数据</text>
    </view>

    <view v-else class="list">
      <uni-list>
        <uni-list-item
          v-for="item in items"
          :key="item.id"
          :title="item.title"
          :note="formatDate(item.created_at)"
          showArrow
        />
      </uni-list>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listItems, type Item } from '../../api/items'

const items = ref<Item[]>([])
const loading = ref(false)

// 加载列表数据
async function loadItems() {
  loading.value = true
  try {
    items.value = await listItems()
  } catch (error) {
    console.error('加载列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 跳转到新增页面
function goToCreate() {
  uni.navigateTo({
    url: '/pages/items/create'
  })
}

// 格式化日期
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 页面显示时刷新列表
onMounted(() => {
  loadItems()
})

// 监听页面显示（从新增页返回时刷新）
uni.onShow(() => {
  loadItems()
})

// 下拉刷新
uni.onPullDownRefresh(() => {
  loadItems().then(() => {
    uni.stopPullDownRefresh()
  })
})
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 30rpx;
  background-color: #fff;
  border-bottom: 1rpx solid #e5e5e5;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.add-btn {
  padding: 10rpx 30rpx;
}

.loading,
.empty {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 100rpx 0;
  color: #999;
  font-size: 28rpx;
}

.list {
  margin-top: 20rpx;
}
</style>
