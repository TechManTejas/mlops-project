import { useMemo, useState, useEffect } from 'react'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [serviceStatus, setServiceStatus] = useState({ status: 'unknown', model_version: 'unknown', model_loaded: false })

  const annotatedImageUrl = useMemo(() => {
    if (!result?.annotated_image_base64) return ''
    return `data:image/jpeg;base64,${result.annotated_image_base64}`
  }, [result])

  useEffect(() => {
    const fetchServiceStatus = async () => {
      try {
        const response = await fetch('/health')
        if (response.ok) {
          const data = await response.json()
          setServiceStatus(data)
        }
      } catch (err) {
        console.error('Failed to fetch service status:', err)
      }
    }

    fetchServiceStatus()
    const interval = setInterval(fetchServiceStatus, 10000) // Poll every 10 seconds
    return () => clearInterval(interval)
  }, [])

  const onFileChange = (event) => {
    const file = event.target.files?.[0]
    setSelectedFile(file ?? null)
    setResult(null)
    setError('')
    if (!file) {
      setPreviewUrl('')
      return
    }
    setPreviewUrl(URL.createObjectURL(file))
  }

  const onSubmit = async (event) => {
    event.preventDefault()
    if (!selectedFile) {
      setError('Please choose an image first.')
      return
    }

    const formData = new FormData()
    formData.append('image', selectedFile)

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const text = await response.text()
        throw new Error(text || 'Prediction request failed.')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Unexpected error occurred.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <header className="header">
        <h1>Parking Detector UI</h1>
        <p>Upload an image and get annotated output from active production model.</p>
        <div className="service-status">
          <span className={`status-indicator ${serviceStatus.model_loaded ? 'ready' : 'not-ready'}`}></span>
          <span>Model: {serviceStatus.model_version}</span>
          <span>Status: {serviceStatus.status}</span>
        </div>
      </header>

      <section className="card form-card">
        <form onSubmit={onSubmit}>
          <div className="field-row">
            <label htmlFor="imageInput">Image</label>
            <input
              id="imageInput"
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              onChange={onFileChange}
            />
          </div>

          <button type="submit" disabled={loading || !serviceStatus.model_loaded}>
            {loading ? 'Running Inference...' : !serviceStatus.model_loaded ? 'Model Not Ready' : 'Run Detection'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
      </section>

      <section className="results-grid">
        <div className="card">
          <h2>Input</h2>
          <div className="image-wrap">
            {previewUrl ? (
              <img src={previewUrl} alt="Input preview" />
            ) : (
              <p className="placeholder">Upload an image to preview.</p>
            )}
          </div>
        </div>

        <div className="card">
          <h2>Annotated Output</h2>
          <div className="image-wrap">
            {annotatedImageUrl ? (
              <img src={annotatedImageUrl} alt="Annotated prediction output" />
            ) : (
              <p className="placeholder">Run detection to see highlighted boxes.</p>
            )}
          </div>
          {result && (
            <div className="meta">
              <span>Model: {result.model_version}</span>
              <span>Time: {result.inference_time}s</span>
              <span>Detections: {result.detections}</span>
              <span className={`status ${result.status}`}>{result.status}</span>
            </div>
          )}
        </div>
      </section>
    </main>
  )
}

export default App
