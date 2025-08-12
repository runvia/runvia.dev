import { JSX } from "react";
import HealthCheck from "../components/HealthCheck";

export default function Projects(): JSX.Element {
  return (
    <div className="text-center">
      <h2 className="text-4xl font-extrabold mb-4">Projects on runvia.dev</h2>
      <p className="text-lg text-gray-600">Your API is <strong>OK</strong> below:</p>
      <HealthCheck />
    </div>
  );
}
