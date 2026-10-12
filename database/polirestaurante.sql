-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema 
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema 
-- -----------------------------------------------------

USE `bxfmuugqxfy2ewefeias` ;

-- -----------------------------------------------------
-- Table ``.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Usuario` (
  `idUsuario` INT NOT NULL,
  `nombre` VARCHAR(100) NULL,
  `credenciales` VARCHAR(255) NULL,
  `estado` VARCHAR(20) NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`idUsuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Mesero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Mesero` (
  `id_mesero` INT NOT NULL,
  `zona_asignada` VARCHAR(45) NULL,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`id_mesero`),
  INDEX `fk_Mesero_Usuario1_idx` (`Usuario_idUsuario` ASC),
  CONSTRAINT `fk_Mesero_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Repartidor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Repartidor` (
  `id_repartidor` INT NOT NULL,
  `placa_vehiculo` VARCHAR(45) NULL,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`id_repartidor`),
  INDEX `fk_Repartidor_Usuario1_idx` (`Usuario_idUsuario` ASC),
  CONSTRAINT `fk_Repartidor_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cliente` (
  `id_cliente` INT NOT NULL,
  `nombre` VARCHAR(45) NULL,
  `direccion` VARCHAR(45) NULL,
  `telefono` VARCHAR(45) NULL,
  PRIMARY KEY (`id_cliente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Pedido` (
  `id_pedido` INT NOT NULL,
  `estado` VARCHAR(45) NULL,
  `fecha_creacion` DATETIME NULL,
  `fecha_ultima_actualizacion` DATETIME NULL,
  `tipo_pedido` VARCHAR(45) NULL,
  `Mesero_id_mesero` INT NULL,
  `Repartidor_id_repartidor` INT NULL,
  `Cliente_id_cliente` INT NULL,
  PRIMARY KEY (`id_pedido`),
  INDEX `fk_Pedido_Mesero1_idx` (`Mesero_id_mesero` ASC),
  INDEX `fk_Pedido_Repartidor1_idx` (`Repartidor_id_repartidor` ASC),
  INDEX `fk_Pedido_Cliente1_idx` (`Cliente_id_cliente` ASC),
  CONSTRAINT `fk_Pedido_Mesero1`
    FOREIGN KEY (`Mesero_id_mesero`)
    REFERENCES `Mesero` (`id_mesero`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedido_Repartidor1`
    FOREIGN KEY (`Repartidor_id_repartidor`)
    REFERENCES `Repartidor` (`id_repartidor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedido_Cliente1`
    FOREIGN KEY (`Cliente_id_cliente`)
    REFERENCES `Cliente` (`id_cliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Mesa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Mesa` (
  `id_mesa` INT NOT NULL,
  `numero` INT NULL,
  `estado` VARCHAR(45) NULL,
  PRIMARY KEY (`id_mesa`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Categoria` (
  `id_categoria` INT NOT NULL,
  `nombre` VARCHAR(100) NULL,
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Producto` (
  `idProducto` INT NOT NULL,
  `nombre` VARCHAR(100) NULL,
  `descripcion` VARCHAR(100) NULL,
  `precio` DOUBLE NULL,
  `cantidad_disponible` INT NULL,
  `Categoria_id_categoria` INT NOT NULL,
  PRIMARY KEY (`idProducto`),
  INDEX `fk_Producto_Categoria2_idx` (`Categoria_id_categoria` ASC),
  CONSTRAINT `fk_Producto_Categoria2`
    FOREIGN KEY (`Categoria_id_categoria`)
    REFERENCES `Categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`DetallePedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DetallePedido` (
  `id_detalle_pedido` INT NOT NULL,
  `cantidad` INT NULL,
  `notas` VARCHAR(120) NULL,
  `Pedido_id_pedido` INT NOT NULL,
  `Producto_idProducto` INT NOT NULL,
  PRIMARY KEY (`id_detalle_pedido`),
  INDEX `fk_DetallePedido_Pedido1_idx` (`Pedido_id_pedido` ASC),
  INDEX `fk_DetallePedido_Producto1_idx` (`Producto_idProducto` ASC),
  CONSTRAINT `fk_DetallePedido_Pedido1`
    FOREIGN KEY (`Pedido_id_pedido`)
    REFERENCES `Pedido` (`id_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DetallePedido_Producto1`
    FOREIGN KEY (`Producto_idProducto`)
    REFERENCES `Producto` (`idProducto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Cajero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cajero` (
  `id_cajero` INT NOT NULL,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`id_cajero`),
  INDEX `fk_Cajero_Usuario1_idx` (`Usuario_idUsuario` ASC),
  CONSTRAINT `fk_Cajero_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Caja`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caja` (
  `id_caja` INT NOT NULL,
  `fecha_apertura` DATETIME NULL,
  `fecha_cierre` DATETIME NULL,
  `monto_inicial` DOUBLE NULL,
  `monto_final` DOUBLE NULL,
  `Cajero_id_cajero` INT NOT NULL,
  PRIMARY KEY (`id_caja`),
  INDEX `fk_Caja_Cajero1_idx` (`Cajero_id_cajero` ASC),
  CONSTRAINT `fk_Caja_Cajero1`
    FOREIGN KEY (`Cajero_id_cajero`)
    REFERENCES `Cajero` (`id_cajero`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Pago`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Pago` (
  `id_pago` INT NOT NULL,
  `monto` DOUBLE NULL,
  `metodo_pago` VARCHAR(45) NULL,
  `fecha_pago` DATETIME NULL,
  `Pedido_id_pedido` INT NOT NULL,
  `Caja_id_caja` INT NOT NULL,
  PRIMARY KEY (`id_pago`),
  INDEX `fk_Pago_Pedido1_idx` (`Pedido_id_pedido` ASC),
  INDEX `fk_Pago_Caja1_idx` (`Caja_id_caja` ASC),
  CONSTRAINT `fk_Pago_Pedido1`
    FOREIGN KEY (`Pedido_id_pedido`)
    REFERENCES `Pedido` (`id_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pago_Caja1`
    FOREIGN KEY (`Caja_id_caja`)
    REFERENCES `Caja` (`id_caja`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Cocinero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cocinero` (
  `id_cocinero` INT NOT NULL,
  `estacion` VARCHAR(45) NULL,
  `Usuario_idUsuario` INT NOT NULL,
  PRIMARY KEY (`id_cocinero`),
  INDEX `fk_Cocinero_Usuario1_idx` (`Usuario_idUsuario` ASC),
  CONSTRAINT `fk_Cocinero_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`PedidoMesa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `PedidoMesa` (
  `id_pedido_mesa` INT NOT NULL,
  `Mesa_id_mesa` INT NOT NULL,
  `Pedido_id_pedido` INT NOT NULL,
  PRIMARY KEY (`id_pedido_mesa`),
  INDEX `fk_PedidoMesa_Mesa1_idx` (`Mesa_id_mesa` ASC),
  INDEX `fk_PedidoMesa_Pedido1_idx` (`Pedido_id_pedido` ASC),
  CONSTRAINT `fk_PedidoMesa_Mesa1`
    FOREIGN KEY (`Mesa_id_mesa`)
    REFERENCES `Mesa` (`id_mesa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PedidoMesa_Pedido1`
    FOREIGN KEY (`Pedido_id_pedido`)
    REFERENCES `Pedido` (`id_pedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Administrador`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Administrador` (
  `id_administrador` INT NOT NULL,
  `Usuario_idUsuario` INT NOT NULL,
  INDEX `fk_Administrador_Usuario1_idx` (`Usuario_idUsuario` ASC),
  PRIMARY KEY (`id_administrador`),
  CONSTRAINT `fk_Administrador_Usuario1`
    FOREIGN KEY (`Usuario_idUsuario`)
    REFERENCES `Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`Reservacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Reservacion` (
  `id_reservacion` INT NOT NULL,
  `fecha` DATETIME NULL,
  `hora` DATETIME NULL,
  `numero_personas` INT NULL,
  `estado` VARCHAR(45) NULL,
  `Cliente_id_cliente` INT NOT NULL,
  PRIMARY KEY (`id_reservacion`),
  INDEX `fk_Reservacion_Cliente1_idx` (`Cliente_id_cliente` ASC),
  CONSTRAINT `fk_Reservacion_Cliente1`
    FOREIGN KEY (`Cliente_id_cliente`)
    REFERENCES `Cliente` (`id_cliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`ReservacionMesa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ReservacionMesa` (
  `id_reservacion_mesa` INT NOT NULL,
  `Mesa_id_mesa` INT NOT NULL,
  `Reservacion_id_reservacion` INT NOT NULL,
  PRIMARY KEY (`id_reservacion_mesa`),
  INDEX `fk_ReservacionMesa_Mesa1_idx` (`Mesa_id_mesa` ASC),
  INDEX `fk_ReservacionMesa_Reservacion1_idx` (`Reservacion_id_reservacion` ASC),
  CONSTRAINT `fk_ReservacionMesa_Mesa1`
    FOREIGN KEY (`Mesa_id_mesa`)
    REFERENCES `Mesa` (`id_mesa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ReservacionMesa_Reservacion1`
    FOREIGN KEY (`Reservacion_id_reservacion`)
    REFERENCES `Reservacion` (`id_reservacion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
