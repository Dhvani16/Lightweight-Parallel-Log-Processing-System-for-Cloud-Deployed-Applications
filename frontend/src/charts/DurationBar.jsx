import { Bar } from "react-chartjs-2";

export default function DurationBar({ duration }) {
  const data = {
    labels: ["Execution Time (ms)"],
    datasets: [
      {
        label: "Job Duration",
        data: [duration],
      },
    ],
  };

  return <Bar data={data} />;
}