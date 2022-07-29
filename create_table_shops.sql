CREATE TABLE `shops` (
  `Id` int(11) NOT NULL,
  `Nome` varchar(200) NULL,
  `Marca` varchar(200) NULL,

  `Distrito` varchar(200) NULL,
  `Municipio` varchar(200) NULL,
  `Morada` varchar(200) NULL,
  `Localidade` varchar(200) NULL,
  `CodPostal` varchar(200) NULL,
  
  `Latitude` decimal(8,6) NULL,
  `Longitude` decimal(9,6) NULL,

  `Gasolina_simples` varchar(200) NULL,
  `Gasolina_simples_date` datetime NULL,

  `Gasolina_simples_95` varchar(200) NULL,
  `Gasolina_simples_95_date` datetime NULL,

  `Gasolina_especial_95` varchar(200) NULL,
  `Gasolina_especial_95_date` datetime NULL,

  `Gasolina_98` varchar(200) NULL,
  `Gasolina_98_date` datetime NULL,

  `Gasolina_especial_98` varchar(200) NULL,
  `Gasolina_especial_98_date` datetime NULL,
  
  `Gasolina_aditivada` varchar(200) NULL,
  `Gasolina_aditivada_date` datetime NULL,

  `Gasóleo_simples` varchar(200) NULL,
  `Gasóleo_simples_date` datetime NULL,

  `Gasóleo_especial` varchar(200) NULL,
  `Gasóleo_especial_date` datetime NULL,

  `GPL_Auto` varchar(200) NULL,  
  `GPL_Auto_date` datetime NULL,

  `Biodiesel_B15` varchar(200) NULL,
  `Biodiesel_B15_date` datetime NULL,

  `Gasóleo_colorido` varchar(200) NULL, 
  `Gasóleo_colorido_date` datetime NULL,

  `Gasóleo_de_aquecimento` varchar(200) NULL,
  `Gasóleo_de_aquecimento_date` datetime NULL,

  `Gasolina_de_mistura` varchar(200) NULL,
  `Gasolina_de_mistura_date` datetime NULL,

  `GNC_kg` varchar(200) NULL,
  `GNC_kg_date` datetime NULL,

  `GNC_m3` varchar(200) NULL,
  `GNC_m3_date` datetime NULL,

  `GNL_kg` varchar(200) NULL,
  `GNL_kg_date` datetime NULL,

  `Gasolina_95_setembro_2021` varchar(200) NULL,
  `Gasolina_95_setembro_2021_date` datetime NULL,

  `Gasóleo_setembro_2021` varchar(200) NULL,
  `Gasóleo_setembro_2021_date` datetime NULL,

  `DataAtualizacao` datetime NULL,

  PRIMARY KEY (`Id`)

)DEFAULT CHARSET=utf8mb4;
