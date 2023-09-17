-- temperature_logs.data_logs definition

CREATE TABLE `data_logs` (
  `mac_address` char(17) NOT NULL,
  `log_timestamp` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `temperature` decimal(4,2) NOT NULL,
  `humidity` decimal(3,2) NOT NULL,
  `battery` decimal(4,3) NOT NULL,
  PRIMARY KEY (`mac_address`,`log_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;