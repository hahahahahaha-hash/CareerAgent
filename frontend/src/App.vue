<template>
  <div class="app">
    <!-- 左侧导航 -->
    <aside class="sidebar">
      <div class="logo">
        CareerAgent
      </div>

      <div class="menu-item" :class="{ active: currentPage === 'career' }" @click="currentPage = 'career'">
        求职分析
      </div>

      <div class="menu-item" :class="{ active: currentPage === 'resume' }" @click="currentPage = 'resume'">
        我的简历
      </div>
    </aside>

    <!-- 右侧主区域 -->
    <main class="main">
      <header class="header">
        <div>
          <h1>AI 求职助手</h1>
          <p>让 AI 帮你分析岗位、匹配技能与简历</p>
        </div>
      </header>

      <section class="content">

        <!-- JD 输入区域 -->
        <div v-if="currentPage === 'career'">
          <el-card class="jd-card">
            <template #header>
              <div class="card-title">
                <span>职位 JD</span>
              </div>
            </template>

            <el-input v-model="jdText" type="textarea" :rows="10"
              placeholder="请粘贴招聘岗位 JD，例如：&#10;&#10;岗位：AI Agent 开发工程师&#10;要求：熟悉 Python、LangChain、LangGraph、RAG..." />

            <div class="action">
              <el-button type="primary" size="large" @click="analyzeJD">
                开始分析
              </el-button>
            </div>
          </el-card>

          <!-- 分析结果 -->

          <el-card>
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>分析结果</div>
                <div>
                  <el-button type="primary"  :loading="reportDownloading" @click="downloadReport">下载</el-button>
                </div>
              </div>
            </template>

            <div class="empty" v-if="result == null || result === ''">
              等待分析...
            </div>
            <div v-else class="report markdown-body" v-html="renderedResult"></div>
          </el-card>
        </div>

        <!-- 我的简历 -->
        <div v-else-if="currentPage === 'resume'">
          <div class="resume-page">

            <el-card class="resume-card">

              <template #header>
                <div class="card-header">
                  <span>我的简历</span>

                  <el-tag type="success">
                    当前使用
                  </el-tag>
                </div>
              </template>

              <!-- 当前简历 -->
              <div class="resume-info">

                <div class="resume-icon">
                  📄
                </div>

                <div class="resume-detail">

                  <div class="resume-name">
                    {{ currentResumeName }}
                  </div>

                  <div class="resume-meta">
                    当前简历 · RAG 知识库已加载
                  </div>

                </div>

              </div>

              <el-divider />

              <!-- 上传区域 -->
              <div class="upload-area">

                <el-upload drag accept=".pdf" :show-file-list="false" :http-request="handleResumeUpload"
                  :disabled="resumeUploading">

                  <el-icon class="upload-icon">
                    <UploadFilled />
                  </el-icon>

                  <div class="upload-text">
                    {{
                      resumeUploading
                        ? '正在更新简历知识库...'
                        : '将新的简历 PDF 拖到这里'
                    }}
                  </div>

                  <div class="upload-tip">
                    {{
                      resumeUploading
                        ? '正在重新生成向量，请稍候'
                        : '或点击选择文件'
                    }}
                  </div>

                </el-upload>

              </div>

            </el-card>

          </div>

        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref ,computed} from 'vue'
import { ElMessage } from 'element-plus'
import { chat, uploadResume ,downloadReportFile} from './api/career'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import { UploadFilled } from '@element-plus/icons-vue'

const currentPage = ref<'career' |  'resume'>('career')

const jdText = ref('')
const result = ref('')
const loading = ref(false)
const resumeUploading = ref(false)
const currentResumeName = ref('resume.pdf')
const reportDownloading = ref(false)
const md = new MarkdownIt({
  html: false,
  breaks: true,
  linkify: true,
})

//分析简历
const renderedResult = computed(() => {
  const html = md.render(result.value)
  return DOMPurify.sanitize(html)
})

const analyzeJD = async () => {
  if (!jdText.value.trim()) {
    ElMessage.warning('请先输入职位 JD')
    return
  }

  loading.value = true

  try {
    const response = await chat(jdText.value)

    result.value = response.data.answer

    ElMessage.success('分析完成')
  } catch (error) {
    console.error(error)
    ElMessage.error('分析失败，请检查后端服务')
  } finally {
    loading.value = false
  }
}

//上传简历
const handleResumeUpload = async (options: any) => {
  const file = options.file as File

  // 检查文件类型
  if (file.type !== 'application/pdf') {
    ElMessage.error('只能上传 PDF 格式的简历')
    return
  }

  // 检查文件大小
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('简历文件不能超过 10MB')
    return
  }

  resumeUploading.value = true

  try {
    const response = await uploadResume(file)

    if (response.data.success) {
      currentResumeName.value = response.data.filename

      ElMessage.success('简历更换成功，RAG 知识库已更新')
    }
  } catch (error) {
    console.error(error)

    ElMessage.error('简历上传失败')
  } finally {
    resumeUploading.value = false
  }
}

//下载分析结果
const downloadReport = async () => {
  if (!result.value) {
    ElMessage.warning('暂无分析结果')
    return
  }

  reportDownloading.value = true

  try {
    const response = await downloadReportFile(
      result.value
    )

    const blob = new Blob(
      [response.data],
      {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      }
    )

    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')

    link.href = url
    link.download = 'AI岗位匹配分析报告.docx'

    document.body.appendChild(link)

    link.click()

    document.body.removeChild(link)

    window.URL.revokeObjectURL(url)

    ElMessage.success('报告下载成功')
  } catch (error) {
    console.error(error)

    ElMessage.error(
      '报告下载失败'
    )
  } finally {
    reportDownloading.value = false
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.app {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

/* 左侧导航 */
.sidebar {
  width: 220px;
  min-height: 100vh;
  background: #1f2937;
  color: white;
  padding: 24px 16px;
  position: fixed;
}

.logo {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 40px;
  padding: 0 12px;
}

.menu-item {
  padding: 13px 16px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #cbd5e1;
}

.menu-item:hover {
  background: #374151;
}

.menu-item.active {
  background: #409eff;
  color: white;
}

/* 主区域 */
.main {
  flex: 1;
  min-width: 0;
  margin-left: 200px;
}

.header {
  height: 90px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  padding: 0 40px;
}

.header h1 {
  margin: 0 0 6px;
  font-size: 26px;
}

.header p {
  margin: 0;
  color: #6b7280;
}

/* 内容区域 */
.content {
  padding: 30px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.jd-card {
  margin-bottom: 24px;
}

.card-title {
  font-weight: 600;
}

.action {
  margin-top: 20px;
  text-align: right;
}

.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.report-card {
  margin-bottom: 30px;
}

.empty {
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

@media (max-width: 900px) {
  .sidebar {
    width: 180px;
  }

  .content {
    padding: 20px;
  }

  .result-grid {
    grid-template-columns: 1fr;
  }
}

.markdown-body {
  color: #374151;
  font-size: 15px;
  line-height: 1.8;
}

/* 一级标题 */
.markdown-body :deep(h1) {
  font-size: 26px;
  margin: 24px 0 16px;
  color: #111827;
}

/* 二级标题 */
.markdown-body :deep(h2) {
  font-size: 21px;
  margin: 24px 0 14px;
  color: #1f2937;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

/* 三级标题 */
.markdown-body :deep(h3) {
  font-size: 18px;
  margin: 20px 0 10px;
  color: #374151;
}

/* 段落 */
.markdown-body :deep(p) {
  margin: 10px 0;
}

/* 粗体 */
.markdown-body :deep(strong) {
  color: #2563eb;
  font-weight: 600;
}

/* 列表 */
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 24px;
  margin: 12px 0;
}

.markdown-body :deep(li) {
  margin: 6px 0;
}

/* 表格 */
.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.markdown-body :deep(th) {
  background: #f3f4f6;
  color: #374151;
  font-weight: 600;
  text-align: left;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
}

.markdown-body :deep(tr:hover) {
  background: #f9fafb;
}

/* 行内代码 */
.markdown-body :deep(code) {
  padding: 2px 6px;
  border-radius: 4px;
  background: #f3f4f6;
  color: #dc2626;
  font-size: 14px;
}

/* 代码块 */
.markdown-body :deep(pre) {
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  border-radius: 8px;
  background: #1f2937;
  color: #f9fafb;
}

.markdown-body :deep(pre code) {
  padding: 0;
  background: transparent;
  color: inherit;
}

/* 引用 */
.markdown-body :deep(blockquote) {
  margin: 16px 0;
  padding: 10px 16px;
  border-left: 4px solid #409eff;
  background: #f5f9ff;
  color: #6b7280;
}

/* 链接 */
.markdown-body :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.resume-info {
  display: flex;
  align-items: center;
  padding: 20px 0;
}

.resume-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: #fef2f2;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  margin-right: 20px;
}

.resume-name {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.resume-meta {
  margin-top: 8px;
  color: #9ca3af;
  font-size: 14px;
}

.upload-area {
  padding: 20px 0;
}

.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  padding: 40px 20px;
}

.upload-icon {
  font-size: 40px;
  color: #409eff;
  margin-bottom: 12px;
}

.upload-text {
  font-size: 16px;
  color: #374151;
}

.upload-tip {
  margin-top: 8px;
  color: #9ca3af;
  font-size: 13px;
}
</style>
