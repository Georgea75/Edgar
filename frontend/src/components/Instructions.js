import React from 'react'

export default function Instructions () {
  return (
      <div>
          <h1 className="text-xl font-bold">Edgar</h1>
          <p className="py-4 text-sm">
              Edgar is a web application that processes and presents data. Under the hood, it imports the provided data into a Pandas data frame while performing type inference.
              Additionally, it offers users the capability to manually override the inferred types.
          </p>
          <h2 className="font-bold">Instructions:</h2>
          <ul className="py-4 text-sm">
              <li>- Upload a file (CSV/Excel format).</li>
              <li>- View the data.</li>
              <li>- Modify the automatically detected types as needed</li>
          </ul>
      </div>
  )
};
