package TestProject.Item;

import TestProject.TestProject;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.item.Item;
import net.minecraftforge.fml.common.registry.GameRegistry;

public class testitem extends Item{

private final String name = "testitem";

    public testitem() {
        GameRegistry.registerItem(this, name);
        this.setUnlocalizedName(name);
        this.setCreativeTab(CreativeTabs.tabRedstone);
    }
	
	public String getName() {
		return name;
	}

}