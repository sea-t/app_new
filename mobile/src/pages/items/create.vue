<template>
  <view class="container">
    <view class="form">
      <view class="form-item">
        <text class="label">标题</text>
        <uni-easyinput
          v-model="title"
          placeholder="请输入待办事项标题"
          :maxlength="100"
          :clearable="true"
        />
      </view>

      <view class="form-item">
        <text class="hint">最多 100 个字符</text>
      </view>

      <view class="form-item">
        <button
          class="submit-btn"
          type="primary"
          :disabled="submitting"
          @click="handleSubmit"
        >
          {{ submitting ? '提交中...' : '提交' }}
        </button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { createItem } from '../../api/items'

const title = ref('')
const submitting = ref(false)

// 表单校验
function validateForm(): boolean {
  if (!title.value || title.value.trim() === '') {
    uni.showToast({
      title: '请输入标题',
      icon: 'none',
      duration: 2000
    })
    return false
  }

  if (title.value.length > 100) {
    uni.showToast({
      title: '标题不能超过 100 个字符',
      icon: 'none',
      duration: 2000
    })
    return false
  }

  return true
}

// 提交表单
async function handleSubmit() {
  if (!validateForm()) {
    return
  }

  submitting.value = true
  try {
    await createItem(title.value.trim())
    uni.showToast({
      title: '添加成功',
      icon: 'success',
      duration: 1500
    })

    // 延迟返回，让用户看到成功提示
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    console.error('创建失败:', error)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 30rpx;
}

.form {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 40rpx 30rpx;
}

.form-item {
  margin-bottom: 30rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
  font-weight: bold;
}

.hint {
  display: block;
  font-size: 24rpx;
  color: #999;
}

.submit-btn {
  width: 100%;
  margin-top: 40rpx;
}
</style>
