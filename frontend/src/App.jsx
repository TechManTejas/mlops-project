import { useMemo, useState } from 'react'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const annotatedImageUrl = useMemo(() => {
    if (!result?.annotated_image_base64) return ''
    return `data:image/jpeg;base64,${result.annotated_image_base64}`
  }, [result])

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
        <p>Upload an image and get annotated output from the active production model.</p>
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

          <button type="submit" disabled={loading}>
            {loading ? 'Running Inference...' : 'Run Detection'}
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
              <span>Version: {result.model_version}</span>
              <span>Detections: {result.detections}</span>
              <span>{result.message}</span>
            </div>
          )}
        </div>
      </section>
    </main>
  )
}

export default App
