import { useState } from 'react'
import './App.css'

function App() {

  const [file, setFile] = useState(null)
  const [halfCut, setHalfCut] = useState("left")
  const [pagesToRemove, setPagesToRemove] = useState("")
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  const handleProcess = async () => {
      try {
          if (!file) {
              setMessage("Please select a PDF file")
              return
          }

          const formData = new FormData()

          formData.append("file", file)
          formData.append("half_cut", halfCut)

          setMessage("")
          setLoading(true)

          const response = await fetch(
              "https://pdf-editor-8vpd.onrender.com/merge",
              {
                  method: "POST",
                  body: formData
              }
          )

          const blob = await response.blob()

          const url = window.URL.createObjectURL(blob)

          const a = document.createElement("a")

          a.href = url

          const originalName =
              file.name.replace(".pdf", "")

          a.download =
              `${originalName}_processed.pdf`

          document.body.appendChild(a)

          a.click()

          a.remove()

          window.URL.revokeObjectURL(url)
          setLoading(false)
          setMessage("PDF processed successfully")


      }catch (error) {
          setMessage(
      "Something went wrong"
          )
          setLoading(false)
      }
  }

  const handleDelete = async () => {
      try{

          if (!file) {
            setMessage("Please select a PDF file")
            return
          }

          if (!pagesToRemove.trim()) {
            setMessage(
              "Please enter page numbers"
            )
            return
          }

          const formData = new FormData()

          formData.append("file", file)

          formData.append(
            "pages_to_remove",
            pagesToRemove
          )

          setMessage("")
          setLoading(true)

          const response = await fetch(
            "https://pdf-editor-8vpd.onrender.com/delete",
            {
              method: "POST",
              body: formData
            }
          )

          const blob = await response.blob()

          const url = window.URL.createObjectURL(blob)

          const a = document.createElement("a")

          a.href = url

          const originalName =
              file.name.replace(".pdf", "")

          a.download =
              `${originalName}_edited.pdf`

          document.body.appendChild(a)

          a.click()

          a.remove()

          window.URL.revokeObjectURL(url)
          setLoading(false)
          setMessage("Pages deleted successfully")

      }catch (error){
          setMessage(
      "Something went wrong"
          )
          setLoading(false)

      }
  }

  return (
    <div className="container">

      <h1>PDF Editor</h1>

      <p className="message">{message}</p>

      {loading && (
          <p className="loading">
            Processing PDF...
          </p>
      )}

      <div className="card">

        <h2>Upload PDF</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
              setFile(e.target.files[0])
              setMessage("")}}
        />

        <br />
        <br />

        {file && (
          <p>
           Selected: {file.name}
          </p>
        )}

      </div>

      <div className="card">

        <h2>Merge PDF</h2>
        <br />

        <select
          value={halfCut}
          onChange={(e) => setHalfCut(e.target.value)}
        >
          <option value="left">Left</option>
          <option value="right">Right</option>
        </select>

        <br />
        <br />

        <button onClick={handleProcess}
                disabled={loading}>
          Process PDF
        </button>

      </div>

      <div className="card">

        <h2>Delete Pages</h2>
        <br />

        <input
          type="text"
          placeholder="Example: 2,5,7"
          value={pagesToRemove}
          onChange={(e) =>
            setPagesToRemove(e.target.value)
          }
        />

        <br />
        <br />

        <button onClick={handleDelete}
                disabled={loading}>
          Delete Pages
        </button>

      </div>

    </div>
  )
}

export default App