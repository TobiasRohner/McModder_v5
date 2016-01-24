package TestProject.Block;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraftforge.fml.common.registry.GameRegistry;
import TestProject.TestProject;

public class testblock extends Block {
	
	private final String name = "testblock";
	private final float hardness = 2.0F;
	private final float resistance = 10.0F;

	public testblock() {
		super(Material.rock);
		GameRegistry.registerBlock(this, name);
		this.setUnlocalizedName(name);
		this.setCreativeTab(CreativeTabs.tabBlock);
		this.setHardness(hardness);
		this.setResistance(resistance);
		this.setHarvestLevel("pickaxe", 0);
	}

}
