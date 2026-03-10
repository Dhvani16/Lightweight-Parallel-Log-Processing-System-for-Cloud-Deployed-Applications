import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

// Register required components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

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