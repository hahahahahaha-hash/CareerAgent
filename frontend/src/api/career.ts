import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 60000,
})

export interface ChatResponse {
  answer: string
}

export interface ResumeUploadResponse {
  success: boolean
  filename: string
  size: number
  message: string
}

export function chat(message: string) {
  return request.get<ChatResponse>('/chat', {
    params: { message },
  })
}

export function uploadResume(file: File) {
  const formData = new FormData()

  formData.append('file', file)

  return request.post<ResumeUploadResponse>(
    '/resume/upload',
    formData
  )
}

export function downloadReportFile(content: string) {
  return request.post(
    '/report/download',
    {
      content,
    },
    {
      responseType: 'blob',
    }
  )
}