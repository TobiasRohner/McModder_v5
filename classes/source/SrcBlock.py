main = """package <package>;

<imports>

public class <classname> extends Block {
	
	private final String name = "<unlocalizedName>";

	public <classname>() {
		super(<material>);
		GameRegistry.registerBlock(this, name);
		this.setUnlocalizedName(name);
		this.setCreativeTab(<creativeTab>);
		this.setHardness(<hardness>F);
		this.setResistance(<resistance>F);
		this.setHarvestLevel("<tool>", <harvestLevel>);
	}

}
"""

imports = """import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraftforge.fml.common.registry.GameRegistry;"""

commonInit = """<instancename> = new <classname>();"""

clientInit = """"""