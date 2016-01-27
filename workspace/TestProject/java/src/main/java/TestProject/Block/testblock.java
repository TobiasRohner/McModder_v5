package TestProject.Block;

import TestProject.TestProject;
import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraftforge.fml.common.registry.GameRegistry;
import net.minecraft.creativetab.CreativeTabs;

public class testblock extends Block {
	
	private final String name = "testblock";

	public testblock() {
		super(Material.rock);
		GameRegistry.registerBlock(this, name);
		this.setUnlocalizedName(name);
		this.setCreativeTab(CreativeTabs.tabFood);
		this.setHardness(2.0F);
		this.setResistance(10.0F);
		this.setHarvestLevel("pickaxe", 0);
	}
	


}
